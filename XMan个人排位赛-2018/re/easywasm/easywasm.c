#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "easywasm.h"
#define UNLIKELY(x) __builtin_expect(!!(x), 0)
#define LIKELY(x) __builtin_expect(!!(x), 1)

#define TRAP(x) (wasm_rt_trap(WASM_RT_TRAP_##x), 0)

#define FUNC_PROLOGUE                                            \
  if (++wasm_rt_call_stack_depth > WASM_RT_MAX_CALL_STACK_DEPTH) \
    TRAP(EXHAUSTION)

#define FUNC_EPILOGUE --wasm_rt_call_stack_depth

#define UNREACHABLE TRAP(UNREACHABLE)

#define CALL_INDIRECT(table, t, ft, x, ...)          \
  (LIKELY((x) < table.size && table.data[x].func &&  \
          table.data[x].func_type == func_types[ft]) \
       ? ((t)table.data[x].func)(__VA_ARGS__)        \
       : TRAP(CALL_INDIRECT))

#define MEMCHECK(mem, a, t)  \
  if (UNLIKELY((a) + sizeof(t) > mem->size)) TRAP(OOB)

#define DEFINE_LOAD(name, t1, t2, t3)              \
  static inline t3 name(wasm_rt_memory_t* mem, u64 addr) {   \
    MEMCHECK(mem, addr, t1);                       \
    t1 result;                                     \
    memcpy(&result, &mem->data[addr], sizeof(t1)); \
    return (t3)(t2)result;                         \
  }

#define DEFINE_STORE(name, t1, t2)                           \
  static inline void name(wasm_rt_memory_t* mem, u64 addr, t2 value) { \
    MEMCHECK(mem, addr, t1);                                 \
    t1 wrapped = (t1)value;                                  \
    memcpy(&mem->data[addr], &wrapped, sizeof(t1));          \
  }

DEFINE_LOAD(i32_load, u32, u32, u32);
DEFINE_LOAD(i64_load, u64, u64, u64);
DEFINE_LOAD(f32_load, f32, f32, f32);
DEFINE_LOAD(f64_load, f64, f64, f64);
DEFINE_LOAD(i32_load8_s, s8, s32, u32);
DEFINE_LOAD(i64_load8_s, s8, s64, u64);
DEFINE_LOAD(i32_load8_u, u8, u32, u32);
DEFINE_LOAD(i64_load8_u, u8, u64, u64);
DEFINE_LOAD(i32_load16_s, s16, s32, u32);
DEFINE_LOAD(i64_load16_s, s16, s64, u64);
DEFINE_LOAD(i32_load16_u, u16, u32, u32);
DEFINE_LOAD(i64_load16_u, u16, u64, u64);
DEFINE_LOAD(i64_load32_s, s32, s64, u64);
DEFINE_LOAD(i64_load32_u, u32, u64, u64);
DEFINE_STORE(i32_store, u32, u32);
DEFINE_STORE(i64_store, u64, u64);
DEFINE_STORE(f32_store, f32, f32);
DEFINE_STORE(f64_store, f64, f64);
DEFINE_STORE(i32_store8, u8, u32);
DEFINE_STORE(i32_store16, u16, u32);
DEFINE_STORE(i64_store8, u8, u64);
DEFINE_STORE(i64_store16, u16, u64);
DEFINE_STORE(i64_store32, u32, u64);

#define I32_CLZ(x) ((x) ? __builtin_clz(x) : 32)
#define I64_CLZ(x) ((x) ? __builtin_clzll(x) : 64)
#define I32_CTZ(x) ((x) ? __builtin_ctz(x) : 32)
#define I64_CTZ(x) ((x) ? __builtin_ctzll(x) : 64)
#define I32_POPCNT(x) (__builtin_popcount(x))
#define I64_POPCNT(x) (__builtin_popcountll(x))

#define DIV_S(ut, min, x, y)                                 \
   ((UNLIKELY((y) == 0)) ?                TRAP(DIV_BY_ZERO)  \
  : (UNLIKELY((x) == min && (y) == -1)) ? TRAP(INT_OVERFLOW) \
  : (ut)((x) / (y)))

#define REM_S(ut, min, x, y)                                \
   ((UNLIKELY((y) == 0)) ?                TRAP(DIV_BY_ZERO) \
  : (UNLIKELY((x) == min && (y) == -1)) ? 0                 \
  : (ut)((x) % (y)))

#define I32_DIV_S(x, y) DIV_S(u32, INT32_MIN, (s32)x, (s32)y)
#define I64_DIV_S(x, y) DIV_S(u64, INT64_MIN, (s64)x, (s64)y)
#define I32_REM_S(x, y) REM_S(u32, INT32_MIN, (s32)x, (s32)y)
#define I64_REM_S(x, y) REM_S(u64, INT64_MIN, (s64)x, (s64)y)

#define DIVREM_U(op, x, y) \
  ((UNLIKELY((y) == 0)) ? TRAP(DIV_BY_ZERO) : ((x) op (y)))

#define DIV_U(x, y) DIVREM_U(/, x, y)
#define REM_U(x, y) DIVREM_U(%, x, y)

#define ROTL(x, y, mask) \
  (((x) << ((y) & (mask))) | ((x) >> (((mask) - (y) + 1) & (mask))))
#define ROTR(x, y, mask) \
  (((x) >> ((y) & (mask))) | ((x) << (((mask) - (y) + 1) & (mask))))

#define I32_ROTL(x, y) ROTL(x, y, 31)
#define I64_ROTL(x, y) ROTL(x, y, 63)
#define I32_ROTR(x, y) ROTR(x, y, 31)
#define I64_ROTR(x, y) ROTR(x, y, 63)

#define FMIN(x, y)                                          \
   ((UNLIKELY((x) != (x))) ? NAN                            \
  : (UNLIKELY((y) != (y))) ? NAN                            \
  : (UNLIKELY((x) == 0 && (y) == 0)) ? (signbit(x) ? x : y) \
  : (x < y) ? x : y)

#define FMAX(x, y)                                          \
   ((UNLIKELY((x) != (x))) ? NAN                            \
  : (UNLIKELY((y) != (y))) ? NAN                            \
  : (UNLIKELY((x) == 0 && (y) == 0)) ? (signbit(x) ? y : x) \
  : (x > y) ? x : y)

#define TRUNC_S(ut, st, ft, min, max, maxop, x)                             \
   ((UNLIKELY((x) != (x))) ? TRAP(INVALID_CONVERSION)                       \
  : (UNLIKELY((x) < (ft)(min) || (x) maxop (ft)(max))) ? TRAP(INT_OVERFLOW) \
  : (ut)(st)(x))

#define I32_TRUNC_S_F32(x) TRUNC_S(u32, s32, f32, INT32_MIN, INT32_MAX, >=, x)
#define I64_TRUNC_S_F32(x) TRUNC_S(u64, s64, f32, INT64_MIN, INT64_MAX, >=, x)
#define I32_TRUNC_S_F64(x) TRUNC_S(u32, s32, f64, INT32_MIN, INT32_MAX, >,  x)
#define I64_TRUNC_S_F64(x) TRUNC_S(u64, s64, f64, INT64_MIN, INT64_MAX, >=, x)

#define TRUNC_U(ut, ft, max, maxop, x)                                    \
   ((UNLIKELY((x) != (x))) ? TRAP(INVALID_CONVERSION)                     \
  : (UNLIKELY((x) <= (ft)-1 || (x) maxop (ft)(max))) ? TRAP(INT_OVERFLOW) \
  : (ut)(x))

#define I32_TRUNC_U_F32(x) TRUNC_U(u32, f32, UINT32_MAX, >=, x)
#define I64_TRUNC_U_F32(x) TRUNC_U(u64, f32, UINT64_MAX, >=, x)
#define I32_TRUNC_U_F64(x) TRUNC_U(u32, f64, UINT32_MAX, >,  x)
#define I64_TRUNC_U_F64(x) TRUNC_U(u64, f64, UINT64_MAX, >=, x)

#define DEFINE_REINTERPRET(name, t1, t2)  \
  static inline t2 name(t1 x) {           \
    t2 result;                            \
    memcpy(&result, &x, sizeof(result));  \
    return result;                        \
  }

DEFINE_REINTERPRET(f32_reinterpret_i32, u32, f32)
DEFINE_REINTERPRET(i32_reinterpret_f32, f32, u32)
DEFINE_REINTERPRET(f64_reinterpret_i64, u64, f64)
DEFINE_REINTERPRET(i64_reinterpret_f64, f64, u64)


static u32 func_types[7];

static void init_func_types(void) {
  func_types[0] = wasm_rt_register_func_type(1, 0, WASM_RT_I32);
  func_types[1] = wasm_rt_register_func_type(2, 0, WASM_RT_I32, WASM_RT_I32);
  func_types[2] = wasm_rt_register_func_type(1, 1, WASM_RT_I32, WASM_RT_I32);
  func_types[3] = wasm_rt_register_func_type(3, 1, WASM_RT_I32, WASM_RT_I32, WASM_RT_I32, WASM_RT_I32);
  func_types[4] = wasm_rt_register_func_type(3, 0, WASM_RT_I32, WASM_RT_I32, WASM_RT_I32);
  func_types[5] = wasm_rt_register_func_type(0, 0);
  func_types[6] = wasm_rt_register_func_type(0, 1, WASM_RT_F64);
}

static void _to_bytes(u32, u32);
static u32 _to_int32(u32);
static u32 _memcpy(u32, u32, u32);
static u32 _memset(u32, u32, u32);
static u32 _memcmp(u32, u32, u32);
static u32 _strlen(u32);
static void _md5(u32, u32, u32);
static u32 _check(u32);
static void runPostSets(void);
static void __post_instantiate(void);
static f64 f11(void);

static u32 g2;
static u32 g3;
static u32 _flag_enc;
static u32 _k;
static u32 _r;

static void init_globals(void) {
  g2 = 0u;
  g3 = 0u;
  _flag_enc = 0u;
  _k = 1104u;
  _r = 1360u;
}

static void _to_bytes(u32 p0, u32 p1) {
  FUNC_PROLOGUE;
  u32 i0, i1, i2;
  i0 = p1;
  i1 = p0;
  i32_store8(Z_envZ_memory, (u64)(i0), i1);
  i0 = p1;
  i1 = p0;
  i2 = 8u;
  i1 >>= (i2 & 31);
  i32_store8(Z_envZ_memory, (u64)(i0 + 1), i1);
  i0 = p1;
  i1 = p0;
  i2 = 16u;
  i1 >>= (i2 & 31);
  i32_store8(Z_envZ_memory, (u64)(i0 + 2), i1);
  i0 = p1;
  i1 = p0;
  i2 = 24u;
  i1 >>= (i2 & 31);
  i32_store8(Z_envZ_memory, (u64)(i0 + 3), i1);
  FUNC_EPILOGUE;
}

static u32 _to_int32(u32 p0) {
  FUNC_PROLOGUE;
  u32 i0, i1, i2;
  i0 = p0;
  i0 = i32_load8_u(Z_envZ_memory, (u64)(i0 + 1));
  i1 = 8u;
  i0 <<= (i1 & 31);
  i1 = p0;
  i1 = i32_load8_u(Z_envZ_memory, (u64)(i1));
  i0 |= i1;
  i1 = p0;
  i1 = i32_load8_u(Z_envZ_memory, (u64)(i1 + 2));
  i2 = 16u;
  i1 <<= (i2 & 31);
  i0 |= i1;
  i1 = p0;
  i1 = i32_load8_u(Z_envZ_memory, (u64)(i1 + 3));
  i2 = 24u;
  i1 <<= (i2 & 31);
  i0 |= i1;
  FUNC_EPILOGUE;
  return i0;
}

static u32 _memcpy(u32 p0, u32 p1, u32 p2) {
  u32 l0 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2;
  i0 = p2;
  if (i0) {
    L1: 
      i0 = p0;
      i1 = l0;
      i0 += i1;
      i1 = p1;
      i2 = l0;
      i1 += i2;
      i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
      i32_store8(Z_envZ_memory, (u64)(i0), i1);
      i0 = l0;
      i1 = 1u;
      i0 += i1;
      l0 = i0;
      i1 = p2;
      i0 = i0 != i1;
      if (i0) {goto L1;}
  }
  i0 = p0;
  FUNC_EPILOGUE;
  return i0;
}

static u32 _memset(u32 p0, u32 p1, u32 p2) {
  u32 l0 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = p2;
  if (i0) {
    i0 = p1;
    i1 = 255u;
    i0 &= i1;
    l0 = i0;
    i0 = 0u;
    p1 = i0;
    L1: 
      i0 = p0;
      i1 = p1;
      i0 += i1;
      i1 = l0;
      i32_store8(Z_envZ_memory, (u64)(i0), i1);
      i0 = p1;
      i1 = 1u;
      i0 += i1;
      p1 = i0;
      i1 = p2;
      i0 = i0 != i1;
      if (i0) {goto L1;}
  }
  i0 = p0;
  FUNC_EPILOGUE;
  return i0;
}

static u32 _memcmp(u32 p0, u32 p1, u32 p2) {
  u32 l0 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2;
  i0 = p2;
  if (i0) {
    L2: 
      i0 = p0;
      i1 = l0;
      i0 += i1;
      i0 = i32_load8_s(Z_envZ_memory, (u64)(i0));
      i1 = p1;
      i2 = l0;
      i1 += i2;
      i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
      i0 = i0 != i1;
      if (i0) {
        i0 = 1u;
        p0 = i0;
        goto B0;
      }
      i0 = l0;
      i1 = 1u;
      i0 += i1;
      l0 = i0;
      i1 = p2;
      i0 = i0 < i1;
      if (i0) {goto L2;}
    i0 = 0u;
    p0 = i0;
  } else {
    i0 = 0u;
    p0 = i0;
  }
  B0:;
  i0 = p0;
  FUNC_EPILOGUE;
  return i0;
}

static u32 _strlen(u32 p0) {
  u32 l0 = 0, l1 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  L0: 
    i0 = l0;
    i1 = 1u;
    i0 += i1;
    l1 = i0;
    i0 = p0;
    i1 = l0;
    i0 += i1;
    i0 = i32_load8_s(Z_envZ_memory, (u64)(i0));
    if (i0) {
      i0 = l1;
      l0 = i0;
      goto L0;
    }
  i0 = l0;
  FUNC_EPILOGUE;
  return i0;
}

static void _md5(u32 p0, u32 p1, u32 p2) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, 
      l8 = 0, l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2, i3, i4;
  i0 = g2;
  l11 = i0;
  i0 = g2;
  i1 = 4160u;
  i0 += i1;
  g2 = i0;
  i0 = l11;
  i1 = 4294967232u;
  i0 -= i1;
  l5 = i0;
  i0 = p1;
  i1 = 1u;
  i0 += i1;
  l2 = i0;
  l3 = i0;
  L0: 
    i0 = l3;
    i1 = 1u;
    i0 += i1;
    l1 = i0;
    i0 = l3;
    i1 = 63u;
    i0 &= i1;
    i1 = 56u;
    i0 = i0 != i1;
    if (i0) {
      i0 = l1;
      l3 = i0;
      goto L0;
    }
  i0 = l5;
  i1 = p0;
  i2 = p1;
  i0 = _memcpy(i0, i1, i2);
  i0 = l5;
  i1 = p1;
  i0 += i1;
  i1 = 4294967168u;
  i32_store8(Z_envZ_memory, (u64)(i0), i1);
  i0 = l2;
  i1 = l3;
  i0 = i0 < i1;
  if (i0) {
    i0 = l5;
    i1 = l2;
    i0 += i1;
    i1 = 0u;
    i2 = l3;
    i3 = 4294967295u;
    i2 += i3;
    i3 = p1;
    i2 -= i3;
    i0 = _memset(i0, i1, i2);
  }
  i0 = l11;
  l13 = i0;
  i0 = p1;
  i1 = 3u;
  i0 <<= (i1 & 31);
  i1 = l5;
  i2 = l3;
  i1 += i2;
  p0 = i1;
  _to_bytes(i0, i1);
  i0 = p1;
  i1 = 29u;
  i0 >>= (i1 & 31);
  i1 = p0;
  i2 = 4u;
  i1 += i2;
  _to_bytes(i0, i1);
  i0 = l3;
  if (i0) {
    i0 = 271733878u;
    l7 = i0;
    i0 = 2562383102u;
    l8 = i0;
    i0 = 4023233417u;
    l9 = i0;
    i0 = 1732584193u;
    l6 = i0;
    L4: 
      i0 = l5;
      i1 = l12;
      i0 += i1;
      p1 = i0;
      i0 = 0u;
      p0 = i0;
      L5: 
        i0 = l13;
        i1 = p0;
        i2 = 2u;
        i1 <<= (i2 & 31);
        i0 += i1;
        i1 = p1;
        i2 = p0;
        i3 = 2u;
        i2 <<= (i3 & 31);
        i1 += i2;
        i1 = _to_int32(i1);
        i32_store(Z_envZ_memory, (u64)(i0), i1);
        i0 = p0;
        i1 = 1u;
        i0 += i1;
        p0 = i0;
        i1 = 16u;
        i0 = i0 != i1;
        if (i0) {goto L5;}
      i0 = l7;
      p1 = i0;
      i0 = l8;
      l1 = i0;
      i0 = l9;
      p0 = i0;
      i0 = l6;
      l10 = i0;
      i0 = 0u;
      l0 = i0;
      L6: 
        i0 = l0;
        i1 = 16u;
        i0 = i0 < i1;
        if (i0) {
          i0 = p1;
          i1 = p0;
          i2 = 4294967295u;
          i1 ^= i2;
          i0 &= i1;
          i1 = l1;
          i2 = p0;
          i1 &= i2;
          i0 |= i1;
          l4 = i0;
          i0 = l0;
        } else {
          i0 = l0;
          i1 = 32u;
          i0 = i0 < i1;
          if (i0) {
            i0 = p1;
            i1 = p0;
            i0 &= i1;
            i1 = l1;
            i2 = p1;
            i3 = 4294967295u;
            i2 ^= i3;
            i1 &= i2;
            i0 |= i1;
            l4 = i0;
            i0 = l0;
            i1 = 5u;
            i0 *= i1;
            i1 = 1u;
            i0 += i1;
            i1 = 15u;
            i0 &= i1;
            goto B7;
          }
          i0 = l0;
          i1 = 48u;
          i0 = i0 < i1;
          if (i0) {
            i0 = l1;
            i1 = p0;
            i0 ^= i1;
            i1 = p1;
            i0 ^= i1;
            l4 = i0;
            i0 = l0;
            i1 = 3u;
            i0 *= i1;
            i1 = 5u;
            i0 += i1;
            i1 = 15u;
            i0 &= i1;
          } else {
            i0 = p0;
            i1 = p1;
            i2 = 4294967295u;
            i1 ^= i2;
            i0 |= i1;
            i1 = l1;
            i0 ^= i1;
            l4 = i0;
            i0 = l0;
            i1 = 7u;
            i0 *= i1;
            i1 = 15u;
            i0 &= i1;
          }
        }
        B7:;
        l2 = i0;
        i0 = l4;
        i1 = l10;
        i0 += i1;
        i1 = (*Z_envZ_memoryBaseZ_i);
        i2 = 1104u;
        i1 += i2;
        i2 = l0;
        i3 = 2u;
        i2 <<= (i3 & 31);
        i1 += i2;
        i1 = i32_load(Z_envZ_memory, (u64)(i1));
        i0 += i1;
        i1 = l13;
        i2 = l2;
        i3 = 2u;
        i2 <<= (i3 & 31);
        i1 += i2;
        i1 = i32_load(Z_envZ_memory, (u64)(i1));
        i0 += i1;
        l2 = i0;
        i1 = 32u;
        i2 = (*Z_envZ_memoryBaseZ_i);
        i3 = 1360u;
        i2 += i3;
        i3 = l0;
        i4 = 2u;
        i3 <<= (i4 & 31);
        i2 += i3;
        i2 = i32_load(Z_envZ_memory, (u64)(i2));
        l4 = i2;
        i1 -= i2;
        i0 >>= (i1 & 31);
        i1 = l2;
        i2 = l4;
        i1 <<= (i2 & 31);
        i0 |= i1;
        i1 = p0;
        i0 += i1;
        l10 = i0;
        i0 = l0;
        i1 = 1u;
        i0 += i1;
        l0 = i0;
        i1 = 64u;
        i0 = i0 != i1;
        if (i0) {
          i0 = p0;
          i1 = l1;
          l4 = i1;
          i1 = l10;
          p0 = i1;
          i1 = p1;
          l10 = i1;
          l1 = i0;
          i0 = l4;
          p1 = i0;
          goto L6;
        }
      i0 = p1;
      i1 = l6;
      i0 += i1;
      l6 = i0;
      i0 = l10;
      i1 = l9;
      i0 += i1;
      l9 = i0;
      i0 = p0;
      i1 = l8;
      i0 += i1;
      l8 = i0;
      i0 = l1;
      i1 = l7;
      i0 += i1;
      l7 = i0;
      i0 = l12;
      i1 = 4294967232u;
      i0 -= i1;
      l12 = i0;
      i1 = l3;
      i0 = i0 < i1;
      if (i0) {goto L4;}
  } else {
    i0 = 1732584193u;
    l6 = i0;
    i0 = 271733878u;
    l7 = i0;
    i0 = 2562383102u;
    l8 = i0;
    i0 = 4023233417u;
    l9 = i0;
  }
  i0 = l6;
  i1 = p2;
  _to_bytes(i0, i1);
  i0 = l9;
  i1 = p2;
  i2 = 4u;
  i1 += i2;
  _to_bytes(i0, i1);
  i0 = l8;
  i1 = p2;
  i2 = 8u;
  i1 += i2;
  _to_bytes(i0, i1);
  i0 = l7;
  i1 = p2;
  i2 = 12u;
  i1 += i2;
  _to_bytes(i0, i1);
  i0 = l11;
  g2 = i0;
  FUNC_EPILOGUE;
}

static u32 _check(u32 p0) {
  u32 l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, 
      l8 = 0, l9 = 0, l10 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2, i3, i4;
  i0 = g2;
  l6 = i0;
  i0 = g2;
  i1 = 160u;
  i0 += i1;
  g2 = i0;
  i0 = l6;
  l7 = i0;
  i0 = l6;
  i1 = 112u;
  i0 += i1;
  l2 = i0;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1616u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1620u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 4), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1624u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 8), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1628u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 12), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1632u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 16), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1636u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 20), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1640u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 24), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1644u;
  i1 += i2;
  i1 = i32_load(Z_envZ_memory, (u64)(i1));
  i32_store(Z_envZ_memory, (u64)(i0 + 28), i1);
  i0 = l2;
  i1 = (*Z_envZ_memoryBaseZ_i);
  i2 = 1648u;
  i1 += i2;
  i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
  i32_store8(Z_envZ_memory, (u64)(i0 + 32), i1);
  i0 = l6;
  i1 = 4294967232u;
  i0 -= i1;
  l0 = i0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 4), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 8), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 12), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 16), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 20), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 24), i1);
  i0 = l0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 28), i1);
  i0 = l0;
  i1 = 0u;
  i32_store8(Z_envZ_memory, (u64)(i0 + 32), i1);
  i0 = l6;
  i1 = 16u;
  i0 += i1;
  l1 = i0;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 4), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 8), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 12), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 16), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 20), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 24), i1);
  i0 = l1;
  i1 = 0u;
  i32_store(Z_envZ_memory, (u64)(i0 + 28), i1);
  i0 = l1;
  i1 = 0u;
  i32_store8(Z_envZ_memory, (u64)(i0 + 32), i1);
  i0 = p0;
  i0 = _strlen(i0);
  i1 = 32u;
  i0 = i0 == i1;
  if (i0) {
    i0 = l2;
    i1 = 31u;
    i0 += i1;
    l10 = i0;
    L2: 
      i0 = l10;
      i1 = p0;
      i2 = l8;
      i1 += i2;
      i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
      i32_store8(Z_envZ_memory, (u64)(i0), i1);
      i0 = l2;
      i1 = 32u;
      i2 = l7;
      _md5(i0, i1, i2);
      i0 = 0u;
      l3 = i0;
      L3: 
        i0 = l0;
        i1 = l3;
        i2 = 1u;
        i1 <<= (i2 & 31);
        l5 = i1;
        i0 += i1;
        i1 = l7;
        i2 = l3;
        i1 += i2;
        i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
        l4 = i1;
        i2 = 255u;
        i1 &= i2;
        i2 = 4u;
        i1 >>= (i2 & 31);
        l9 = i1;
        i2 = 48u;
        i1 |= i2;
        i2 = l9;
        i3 = 87u;
        i2 += i3;
        i3 = l4;
        i4 = 255u;
        i3 &= i4;
        i4 = 160u;
        i3 = (u32)((s32)i3 < (s32)i4);
        i1 = i3 ? i1 : i2;
        i32_store8(Z_envZ_memory, (u64)(i0), i1);
        i0 = l0;
        i1 = l5;
        i2 = 1u;
        i1 |= i2;
        i0 += i1;
        i1 = l4;
        i2 = 15u;
        i1 &= i2;
        l4 = i1;
        l5 = i1;
        i2 = 48u;
        i1 |= i2;
        i2 = l5;
        i3 = 87u;
        i2 += i3;
        i3 = l4;
        i4 = 10u;
        i3 = (u32)((s32)i3 < (s32)i4);
        i1 = i3 ? i1 : i2;
        i32_store8(Z_envZ_memory, (u64)(i0), i1);
        i0 = l3;
        i1 = 1u;
        i0 += i1;
        l3 = i0;
        i1 = 16u;
        i0 = i0 != i1;
        if (i0) {goto L3;}
      i0 = l0;
      i1 = 32u;
      i2 = l7;
      _md5(i0, i1, i2);
      i0 = 0u;
      l3 = i0;
      L4: 
        i0 = l1;
        i1 = l3;
        i2 = 1u;
        i1 <<= (i2 & 31);
        l5 = i1;
        i0 += i1;
        i1 = l7;
        i2 = l3;
        i1 += i2;
        i1 = i32_load8_s(Z_envZ_memory, (u64)(i1));
        l4 = i1;
        i2 = 255u;
        i1 &= i2;
        i2 = 4u;
        i1 >>= (i2 & 31);
        l9 = i1;
        i2 = 48u;
        i1 |= i2;
        i2 = l9;
        i3 = 87u;
        i2 += i3;
        i3 = l4;
        i4 = 255u;
        i3 &= i4;
        i4 = 160u;
        i3 = (u32)((s32)i3 < (s32)i4);
        i1 = i3 ? i1 : i2;
        i32_store8(Z_envZ_memory, (u64)(i0), i1);
        i0 = l1;
        i1 = l5;
        i2 = 1u;
        i1 |= i2;
        i0 += i1;
        i1 = l4;
        i2 = 15u;
        i1 &= i2;
        l4 = i1;
        l5 = i1;
        i2 = 48u;
        i1 |= i2;
        i2 = l5;
        i3 = 87u;
        i2 += i3;
        i3 = l4;
        i4 = 10u;
        i3 = (u32)((s32)i3 < (s32)i4);
        i1 = i3 ? i1 : i2;
        i32_store8(Z_envZ_memory, (u64)(i0), i1);
        i0 = l3;
        i1 = 1u;
        i0 += i1;
        l3 = i0;
        i1 = 16u;
        i0 = i0 != i1;
        if (i0) {goto L4;}
      i0 = l1;
      i1 = (*Z_envZ_memoryBaseZ_i);
      i2 = l8;
      i3 = 33u;
      i2 *= i3;
      i1 += i2;
      i2 = 32u;
      i0 = _memcmp(i0, i1, i2);
      if (i0) {
        i0 = 0u;
        p0 = i0;
        goto B0;
      }
      i0 = l8;
      i1 = 1u;
      i0 += i1;
      l8 = i0;
      i1 = 32u;
      i0 = i0 < i1;
      if (i0) {goto L2;}
    i0 = 1u;
    p0 = i0;
  } else {
    i0 = 0u;
    p0 = i0;
  }
  B0:;
  i0 = l6;
  g2 = i0;
  i0 = p0;
  FUNC_EPILOGUE;
  return i0;
}

static void runPostSets(void) {
  FUNC_PROLOGUE;
  FUNC_EPILOGUE;
}

static void __post_instantiate(void) {
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = (*Z_envZ_memoryBaseZ_i);
  i1 = 1664u;
  i0 += i1;
  g2 = i0;
  i0 = g2;
  i1 = 5242880u;
  i0 += i1;
  g3 = i0;
  FUNC_EPILOGUE;
}

static f64 f11(void) {
  FUNC_PROLOGUE;
  u32 i0;
  f64 d0;
  i0 = 0u;
  (*Z_envZ_abortZ_vi)(i0);
  d0 = 0;
  FUNC_EPILOGUE;
  return d0;
}

static const u8 data_segment_data_0[] = {
  0x35, 0x36, 0x32, 0x66, 0x65, 0x33, 0x63, 0x63, 0x35, 0x30, 0x30, 0x31, 
  0x34, 0x63, 0x32, 0x36, 0x30, 0x64, 0x39, 0x65, 0x38, 0x63, 0x66, 0x34, 
  0x65, 0x64, 0x33, 0x38, 0x63, 0x37, 0x37, 0x61, 0x00, 0x63, 0x30, 0x32, 
  0x32, 0x61, 0x64, 0x30, 0x63, 0x63, 0x30, 0x30, 0x37, 0x35, 0x61, 0x39, 
  0x61, 0x62, 0x31, 0x34, 0x62, 0x34, 0x31, 0x32, 0x61, 0x31, 0x30, 0x38, 
  0x32, 0x64, 0x35, 0x66, 0x33, 0x00, 0x36, 0x34, 0x63, 0x32, 0x38, 0x36, 
  0x63, 0x66, 0x63, 0x36, 0x32, 0x33, 0x61, 0x61, 0x38, 0x64, 0x37, 0x64, 
  0x66, 0x37, 0x63, 0x30, 0x38, 0x38, 0x65, 0x62, 0x66, 0x37, 0x64, 0x37, 
  0x31, 0x38, 0x00, 0x38, 0x33, 0x36, 0x36, 0x34, 0x62, 0x64, 0x65, 0x65, 
  0x34, 0x62, 0x36, 0x31, 0x33, 0x62, 0x37, 0x65, 0x37, 0x61, 0x35, 0x31, 
  0x62, 0x35, 0x32, 0x31, 0x33, 0x34, 0x37, 0x30, 0x61, 0x38, 0x64, 0x00, 
  0x62, 0x30, 0x32, 0x30, 0x62, 0x66, 0x35, 0x39, 0x38, 0x61, 0x61, 0x61, 
  0x32, 0x62, 0x33, 0x65, 0x30, 0x33, 0x65, 0x64, 0x30, 0x32, 0x63, 0x38, 
  0x35, 0x34, 0x33, 0x36, 0x32, 0x36, 0x38, 0x61, 0x00, 0x34, 0x66, 0x64, 
  0x61, 0x63, 0x35, 0x61, 0x63, 0x38, 0x30, 0x37, 0x35, 0x30, 0x36, 0x39, 
  0x33, 0x38, 0x31, 0x30, 0x33, 0x65, 0x37, 0x37, 0x35, 0x63, 0x35, 0x30, 
  0x30, 0x39, 0x39, 0x65, 0x64, 0x00, 0x34, 0x66, 0x64, 0x61, 0x63, 0x35, 
  0x61, 0x63, 0x38, 0x30, 0x37, 0x35, 0x30, 0x36, 0x39, 0x33, 0x38, 0x31, 
  0x30, 0x33, 0x65, 0x37, 0x37, 0x35, 0x63, 0x35, 0x30, 0x30, 0x39, 0x39, 
  0x65, 0x64, 0x00, 0x63, 0x32, 0x33, 0x31, 0x64, 0x36, 0x30, 0x37, 0x62, 
  0x36, 0x38, 0x32, 0x33, 0x66, 0x64, 0x30, 0x61, 0x36, 0x38, 0x65, 0x38, 
  0x31, 0x33, 0x37, 0x36, 0x30, 0x38, 0x30, 0x39, 0x37, 0x35, 0x34, 0x00, 
  0x64, 0x31, 0x36, 0x38, 0x63, 0x32, 0x31, 0x64, 0x31, 0x30, 0x33, 0x37, 
  0x31, 0x61, 0x35, 0x61, 0x62, 0x36, 0x31, 0x62, 0x63, 0x66, 0x65, 0x36, 
  0x63, 0x37, 0x35, 0x39, 0x65, 0x66, 0x36, 0x65, 0x00, 0x66, 0x36, 0x30, 
  0x64, 0x37, 0x30, 0x39, 0x63, 0x63, 0x66, 0x39, 0x38, 0x39, 0x64, 0x38, 
  0x34, 0x39, 0x30, 0x32, 0x38, 0x66, 0x39, 0x37, 0x61, 0x30, 0x33, 0x64, 
  0x32, 0x66, 0x33, 0x62, 0x61, 0x00, 0x61, 0x30, 0x31, 0x38, 0x34, 0x66, 
  0x38, 0x32, 0x34, 0x30, 0x65, 0x32, 0x66, 0x65, 0x34, 0x36, 0x38, 0x36, 
  0x31, 0x64, 0x63, 0x38, 0x64, 0x31, 0x35, 0x61, 0x38, 0x31, 0x39, 0x63, 
  0x62, 0x30, 0x00, 0x39, 0x64, 0x62, 0x65, 0x63, 0x34, 0x31, 0x34, 0x33, 
  0x33, 0x36, 0x65, 0x37, 0x34, 0x31, 0x65, 0x39, 0x63, 0x37, 0x33, 0x34, 
  0x32, 0x32, 0x64, 0x66, 0x35, 0x39, 0x64, 0x65, 0x32, 0x39, 0x37, 0x00, 
  0x36, 0x66, 0x62, 0x35, 0x32, 0x30, 0x39, 0x64, 0x38, 0x66, 0x63, 0x38, 
  0x62, 0x62, 0x38, 0x35, 0x30, 0x37, 0x32, 0x34, 0x35, 0x62, 0x63, 0x66, 
  0x61, 0x32, 0x34, 0x61, 0x65, 0x31, 0x31, 0x66, 0x00, 0x36, 0x66, 0x62, 
  0x35, 0x32, 0x30, 0x39, 0x64, 0x38, 0x66, 0x63, 0x38, 0x62, 0x62, 0x38, 
  0x35, 0x30, 0x37, 0x32, 0x34, 0x35, 0x62, 0x63, 0x66, 0x61, 0x32, 0x34, 
  0x61, 0x65, 0x31, 0x31, 0x66, 0x00, 0x30, 0x30, 0x63, 0x37, 0x37, 0x66, 
  0x62, 0x63, 0x36, 0x30, 0x61, 0x35, 0x62, 0x66, 0x63, 0x34, 0x36, 0x36, 
  0x64, 0x33, 0x64, 0x30, 0x36, 0x39, 0x38, 0x37, 0x36, 0x65, 0x63, 0x33, 
  0x34, 0x38, 0x00, 0x30, 0x30, 0x63, 0x37, 0x37, 0x66, 0x62, 0x63, 0x36, 
  0x30, 0x61, 0x35, 0x62, 0x66, 0x63, 0x34, 0x36, 0x36, 0x64, 0x33, 0x64, 
  0x30, 0x36, 0x39, 0x38, 0x37, 0x36, 0x65, 0x63, 0x33, 0x34, 0x38, 0x00, 
  0x64, 0x66, 0x33, 0x33, 0x34, 0x36, 0x34, 0x66, 0x62, 0x34, 0x37, 0x31, 
  0x63, 0x34, 0x36, 0x61, 0x62, 0x61, 0x66, 0x36, 0x39, 0x31, 0x63, 0x30, 
  0x30, 0x30, 0x61, 0x30, 0x65, 0x33, 0x30, 0x64, 0x00, 0x34, 0x66, 0x64, 
  0x61, 0x63, 0x35, 0x61, 0x63, 0x38, 0x30, 0x37, 0x35, 0x30, 0x36, 0x39, 
  0x33, 0x38, 0x31, 0x30, 0x33, 0x65, 0x37, 0x37, 0x35, 0x63, 0x35, 0x30, 
  0x30, 0x39, 0x39, 0x65, 0x64, 0x00, 0x66, 0x36, 0x30, 0x64, 0x37, 0x30, 
  0x39, 0x63, 0x63, 0x66, 0x39, 0x38, 0x39, 0x64, 0x38, 0x34, 0x39, 0x30, 
  0x32, 0x38, 0x66, 0x39, 0x37, 0x61, 0x30, 0x33, 0x64, 0x32, 0x66, 0x33, 
  0x62, 0x61, 0x00, 0x66, 0x63, 0x63, 0x39, 0x34, 0x61, 0x32, 0x30, 0x35, 
  0x39, 0x36, 0x66, 0x32, 0x36, 0x31, 0x39, 0x38, 0x36, 0x38, 0x66, 0x33, 
  0x61, 0x34, 0x62, 0x66, 0x35, 0x32, 0x65, 0x61, 0x64, 0x66, 0x37, 0x00, 
  0x30, 0x30, 0x63, 0x37, 0x37, 0x66, 0x62, 0x63, 0x36, 0x30, 0x61, 0x35, 
  0x62, 0x66, 0x63, 0x34, 0x36, 0x36, 0x64, 0x33, 0x64, 0x30, 0x36, 0x39, 
  0x38, 0x37, 0x36, 0x65, 0x63, 0x33, 0x34, 0x38, 0x00, 0x64, 0x31, 0x36, 
  0x38, 0x63, 0x32, 0x31, 0x64, 0x31, 0x30, 0x33, 0x37, 0x31, 0x61, 0x35, 
  0x61, 0x62, 0x36, 0x31, 0x62, 0x63, 0x66, 0x65, 0x36, 0x63, 0x37, 0x35, 
  0x39, 0x65, 0x66, 0x36, 0x65, 0x00, 0x39, 0x64, 0x62, 0x65, 0x63, 0x34, 
  0x31, 0x34, 0x33, 0x33, 0x36, 0x65, 0x37, 0x34, 0x31, 0x65, 0x39, 0x63, 
  0x37, 0x33, 0x34, 0x32, 0x32, 0x64, 0x66, 0x35, 0x39, 0x64, 0x65, 0x32, 
  0x39, 0x37, 0x00, 0x66, 0x63, 0x63, 0x39, 0x34, 0x61, 0x32, 0x30, 0x35, 
  0x39, 0x36, 0x66, 0x32, 0x36, 0x31, 0x39, 0x38, 0x36, 0x38, 0x66, 0x33, 
  0x61, 0x34, 0x62, 0x66, 0x35, 0x32, 0x65, 0x61, 0x64, 0x66, 0x37, 0x00, 
  0x39, 0x62, 0x33, 0x37, 0x64, 0x62, 0x30, 0x39, 0x31, 0x39, 0x37, 0x39, 
  0x62, 0x65, 0x64, 0x66, 0x30, 0x30, 0x61, 0x37, 0x30, 0x39, 0x35, 0x38, 
  0x35, 0x31, 0x62, 0x61, 0x36, 0x66, 0x35, 0x39, 0x00, 0x30, 0x30, 0x63, 
  0x37, 0x37, 0x66, 0x62, 0x63, 0x36, 0x30, 0x61, 0x35, 0x62, 0x66, 0x63, 
  0x34, 0x36, 0x36, 0x64, 0x33, 0x64, 0x30, 0x36, 0x39, 0x38, 0x37, 0x36, 
  0x65, 0x63, 0x33, 0x34, 0x38, 0x00, 0x66, 0x36, 0x30, 0x64, 0x37, 0x30, 
  0x39, 0x63, 0x63, 0x66, 0x39, 0x38, 0x39, 0x64, 0x38, 0x34, 0x39, 0x30, 
  0x32, 0x38, 0x66, 0x39, 0x37, 0x61, 0x30, 0x33, 0x64, 0x32, 0x66, 0x33, 
  0x62, 0x61, 0x00, 0x66, 0x63, 0x63, 0x39, 0x34, 0x61, 0x32, 0x30, 0x35, 
  0x39, 0x36, 0x66, 0x32, 0x36, 0x31, 0x39, 0x38, 0x36, 0x38, 0x66, 0x33, 
  0x61, 0x34, 0x62, 0x66, 0x35, 0x32, 0x65, 0x61, 0x64, 0x66, 0x37, 0x00, 
  0x64, 0x31, 0x36, 0x38, 0x63, 0x32, 0x31, 0x64, 0x31, 0x30, 0x33, 0x37, 
  0x31, 0x61, 0x35, 0x61, 0x62, 0x36, 0x31, 0x62, 0x63, 0x66, 0x65, 0x36, 
  0x63, 0x37, 0x35, 0x39, 0x65, 0x66, 0x36, 0x65, 0x00, 0x66, 0x36, 0x30, 
  0x64, 0x37, 0x30, 0x39, 0x63, 0x63, 0x66, 0x39, 0x38, 0x39, 0x64, 0x38, 
  0x34, 0x39, 0x30, 0x32, 0x38, 0x66, 0x39, 0x37, 0x61, 0x30, 0x33, 0x64, 
  0x32, 0x66, 0x33, 0x62, 0x61, 0x00, 0x31, 0x38, 0x33, 0x33, 0x34, 0x32, 
  0x39, 0x39, 0x37, 0x66, 0x66, 0x65, 0x64, 0x34, 0x62, 0x33, 0x31, 0x38, 
  0x39, 0x65, 0x39, 0x37, 0x37, 0x64, 0x30, 0x37, 0x37, 0x61, 0x36, 0x30, 
  0x62, 0x34, 0x00, 0x66, 0x34, 0x30, 0x34, 0x61, 0x33, 0x33, 0x36, 0x38, 
  0x64, 0x32, 0x64, 0x38, 0x66, 0x35, 0x37, 0x34, 0x36, 0x34, 0x66, 0x37, 
  0x33, 0x39, 0x64, 0x34, 0x65, 0x64, 0x30, 0x31, 0x63, 0x30, 0x65, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x78, 0xa4, 0x6a, 0xd7, 0x56, 0xb7, 0xc7, 0xe8, 0xdb, 0x70, 0x20, 0x24, 
  0xee, 0xce, 0xbd, 0xc1, 0xaf, 0x0f, 0x7c, 0xf5, 0x2a, 0xc6, 0x87, 0x47, 
  0x13, 0x46, 0x30, 0xa8, 0x01, 0x95, 0x46, 0xfd, 0xd8, 0x98, 0x80, 0x69, 
  0xaf, 0xf7, 0x44, 0x8b, 0xb1, 0x5b, 0xff, 0xff, 0xbe, 0xd7, 0x5c, 0x89, 
  0x22, 0x11, 0x90, 0x6b, 0x93, 0x71, 0x98, 0xfd, 0x8e, 0x43, 0x79, 0xa6, 
  0x21, 0x08, 0xb4, 0x49, 0x62, 0x25, 0x1e, 0xf6, 0x40, 0xb3, 0x40, 0xc0, 
  0x51, 0x5a, 0x5e, 0x26, 0xaa, 0xc7, 0xb6, 0xe9, 0x5d, 0x10, 0x2f, 0xd6, 
  0x53, 0x14, 0x44, 0x02, 0x81, 0xe6, 0xa1, 0xd8, 0xc8, 0xfb, 0xd3, 0xe7, 
  0xe6, 0xcd, 0xe1, 0x21, 0xd6, 0x07, 0x37, 0xc3, 0x87, 0x0d, 0xd5, 0xf4, 
  0xed, 0x14, 0x5a, 0x45, 0x05, 0xe9, 0xe3, 0xa9, 0xf8, 0xa3, 0xef, 0xfc, 
  0xd9, 0x02, 0x6f, 0x67, 0x8a, 0x4c, 0x2a, 0x8d, 0x42, 0x39, 0xfa, 0xff, 
  0x81, 0xf6, 0x71, 0x87, 0x22, 0x61, 0x9d, 0x6d, 0x0c, 0x38, 0xe5, 0xfd, 
  0x44, 0xea, 0xbe, 0xa4, 0xa9, 0xcf, 0xde, 0x4b, 0x60, 0x4b, 0xbb, 0xf6, 
  0x70, 0xbc, 0xbf, 0xbe, 0xc6, 0x7e, 0x9b, 0x28, 0xfa, 0x27, 0xa1, 0xea, 
  0x85, 0x30, 0xef, 0xd4, 0x05, 0x1d, 0x88, 0x04, 0x39, 0xd0, 0xd4, 0xd9, 
  0xe5, 0x99, 0xdb, 0xe6, 0xf8, 0x7c, 0xa2, 0x1f, 0x65, 0x56, 0xac, 0xc4, 
  0x44, 0x22, 0x29, 0xf4, 0x97, 0xff, 0x2a, 0x43, 0xa7, 0x23, 0x94, 0xab, 
  0x39, 0xa0, 0x93, 0xfc, 0xc3, 0x59, 0x5b, 0x65, 0x92, 0xcc, 0x0c, 0x8f, 
  0x7d, 0xf4, 0xef, 0xff, 0xd1, 0x5d, 0x84, 0x85, 0x4f, 0x7e, 0xa8, 0x6f, 
  0xe0, 0xe6, 0x2c, 0xfe, 0x14, 0x43, 0x01, 0xa3, 0xa1, 0x11, 0x08, 0x4e, 
  0x82, 0x7e, 0x53, 0xf7, 0x35, 0xf2, 0x3a, 0xbd, 0xbb, 0xd2, 0xd7, 0x2a, 
  0x91, 0xd3, 0x86, 0xeb, 0x07, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 
  0x11, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
  0x0c, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 
  0x07, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 
  0x16, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 
  0x11, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 
  0x09, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 
  0x05, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 
  0x14, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 
  0x0e, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 
  0x09, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 
  0x04, 0x00, 0x00, 0x00, 0x0b, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 
  0x17, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x0b, 0x00, 0x00, 0x00, 
  0x10, 0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
  0x0b, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 
  0x04, 0x00, 0x00, 0x00, 0x0b, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 
  0x17, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 
  0x0f, 0x00, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 
  0x0a, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 
  0x06, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 
  0x15, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 
  0x0f, 0x00, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x32, 0x33, 0x33, 0x33, 
  0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 
  0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 
  0x33, 0x33, 0x33, 0x33, 
};

static void init_memory(void) {
  memcpy(&((*Z_envZ_memory).data[(*Z_envZ_memoryBaseZ_i)]), data_segment_data_0, 1648);
}

static void init_table(void) {
  uint32_t offset;
  offset = (*Z_envZ_tableBaseZ_i);
  (*Z_envZ_table).data[offset + 0] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 1] = (wasm_rt_elem_t){func_types[1], (wasm_rt_anyfunc_t)(&_to_bytes)};
  (*Z_envZ_table).data[offset + 2] = (wasm_rt_elem_t){func_types[2], (wasm_rt_anyfunc_t)(&_to_int32)};
  (*Z_envZ_table).data[offset + 3] = (wasm_rt_elem_t){func_types[3], (wasm_rt_anyfunc_t)(&_memcpy)};
  (*Z_envZ_table).data[offset + 4] = (wasm_rt_elem_t){func_types[3], (wasm_rt_anyfunc_t)(&_memset)};
  (*Z_envZ_table).data[offset + 5] = (wasm_rt_elem_t){func_types[3], (wasm_rt_anyfunc_t)(&_memcmp)};
  (*Z_envZ_table).data[offset + 6] = (wasm_rt_elem_t){func_types[2], (wasm_rt_anyfunc_t)(&_strlen)};
  (*Z_envZ_table).data[offset + 7] = (wasm_rt_elem_t){func_types[4], (wasm_rt_anyfunc_t)(&_md5)};
  (*Z_envZ_table).data[offset + 8] = (wasm_rt_elem_t){func_types[2], (wasm_rt_anyfunc_t)(&_check)};
  (*Z_envZ_table).data[offset + 9] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 10] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 11] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 12] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 13] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 14] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
  (*Z_envZ_table).data[offset + 15] = (wasm_rt_elem_t){func_types[6], (wasm_rt_anyfunc_t)(&f11)};
}

/* export: '__post_instantiate' */
void (*WASM_RT_ADD_PREFIX(Z___post_instantiateZ_vv))(void);
/* export: '_check' */
u32 (*WASM_RT_ADD_PREFIX(Z__checkZ_ii))(u32);
/* export: '_md5' */
void (*WASM_RT_ADD_PREFIX(Z__md5Z_viii))(u32, u32, u32);
/* export: '_memcmp' */
u32 (*WASM_RT_ADD_PREFIX(Z__memcmpZ_iiii))(u32, u32, u32);
/* export: '_memcpy' */
u32 (*WASM_RT_ADD_PREFIX(Z__memcpyZ_iiii))(u32, u32, u32);
/* export: '_memset' */
u32 (*WASM_RT_ADD_PREFIX(Z__memsetZ_iiii))(u32, u32, u32);
/* export: '_strlen' */
u32 (*WASM_RT_ADD_PREFIX(Z__strlenZ_ii))(u32);
/* export: '_to_bytes' */
void (*WASM_RT_ADD_PREFIX(Z__to_bytesZ_vii))(u32, u32);
/* export: '_to_int32' */
u32 (*WASM_RT_ADD_PREFIX(Z__to_int32Z_ii))(u32);
/* export: 'runPostSets' */
void (*WASM_RT_ADD_PREFIX(Z_runPostSetsZ_vv))(void);
/* export: '_flag_enc' */
u32 (*WASM_RT_ADD_PREFIX(Z__flag_encZ_i));
/* export: '_k' */
u32 (*WASM_RT_ADD_PREFIX(Z__kZ_i));
/* export: '_r' */
u32 (*WASM_RT_ADD_PREFIX(Z__rZ_i));

static void init_exports(void) {
  /* export: '__post_instantiate' */
  WASM_RT_ADD_PREFIX(Z___post_instantiateZ_vv) = (&__post_instantiate);
  /* export: '_check' */
  WASM_RT_ADD_PREFIX(Z__checkZ_ii) = (&_check);
  /* export: '_md5' */
  WASM_RT_ADD_PREFIX(Z__md5Z_viii) = (&_md5);
  /* export: '_memcmp' */
  WASM_RT_ADD_PREFIX(Z__memcmpZ_iiii) = (&_memcmp);
  /* export: '_memcpy' */
  WASM_RT_ADD_PREFIX(Z__memcpyZ_iiii) = (&_memcpy);
  /* export: '_memset' */
  WASM_RT_ADD_PREFIX(Z__memsetZ_iiii) = (&_memset);
  /* export: '_strlen' */
  WASM_RT_ADD_PREFIX(Z__strlenZ_ii) = (&_strlen);
  /* export: '_to_bytes' */
  WASM_RT_ADD_PREFIX(Z__to_bytesZ_vii) = (&_to_bytes);
  /* export: '_to_int32' */
  WASM_RT_ADD_PREFIX(Z__to_int32Z_ii) = (&_to_int32);
  /* export: 'runPostSets' */
  WASM_RT_ADD_PREFIX(Z_runPostSetsZ_vv) = (&runPostSets);
  /* export: '_flag_enc' */
  WASM_RT_ADD_PREFIX(Z__flag_encZ_i) = (&_flag_enc);
  /* export: '_k' */
  WASM_RT_ADD_PREFIX(Z__kZ_i) = (&_k);
  /* export: '_r' */
  WASM_RT_ADD_PREFIX(Z__rZ_i) = (&_r);
}

void WASM_RT_ADD_PREFIX(init)(void) {
  init_func_types();
  init_globals();
  init_memory();
  init_table();
  init_exports();
}
