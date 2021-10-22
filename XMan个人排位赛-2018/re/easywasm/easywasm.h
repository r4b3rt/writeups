#ifndef EASYWASM_H_GENERATED_
#define EASYWASM_H_GENERATED_
#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

#include "wasm-rt.h"

#ifndef WASM_RT_MODULE_PREFIX
#define WASM_RT_MODULE_PREFIX
#endif

#define WASM_RT_PASTE_(x, y) x ## y
#define WASM_RT_PASTE(x, y) WASM_RT_PASTE_(x, y)
#define WASM_RT_ADD_PREFIX(x) WASM_RT_PASTE(WASM_RT_MODULE_PREFIX, x)

/* TODO(binji): only use stdint.h types in header */
typedef uint8_t u8;
typedef int8_t s8;
typedef uint16_t u16;
typedef int16_t s16;
typedef uint32_t u32;
typedef int32_t s32;
typedef uint64_t u64;
typedef int64_t s64;
typedef float f32;
typedef double f64;

extern void WASM_RT_ADD_PREFIX(init)(void);

/* import: 'env' 'memory' */
extern wasm_rt_memory_t (*Z_envZ_memory);
/* import: 'env' 'table' */
extern wasm_rt_table_t (*Z_envZ_table);
/* import: 'env' 'memoryBase' */
extern u32 (*Z_envZ_memoryBaseZ_i);
/* import: 'env' 'tableBase' */
extern u32 (*Z_envZ_tableBaseZ_i);
/* import: 'env' 'abort' */
extern void (*Z_envZ_abortZ_vi)(u32);

/* export: '__post_instantiate' */
extern void (*WASM_RT_ADD_PREFIX(Z___post_instantiateZ_vv))(void);
/* export: '_check' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__checkZ_ii))(u32);
/* export: '_md5' */
extern void (*WASM_RT_ADD_PREFIX(Z__md5Z_viii))(u32, u32, u32);
/* export: '_memcmp' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__memcmpZ_iiii))(u32, u32, u32);
/* export: '_memcpy' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__memcpyZ_iiii))(u32, u32, u32);
/* export: '_memset' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__memsetZ_iiii))(u32, u32, u32);
/* export: '_strlen' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__strlenZ_ii))(u32);
/* export: '_to_bytes' */
extern void (*WASM_RT_ADD_PREFIX(Z__to_bytesZ_vii))(u32, u32);
/* export: '_to_int32' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__to_int32Z_ii))(u32);
/* export: 'runPostSets' */
extern void (*WASM_RT_ADD_PREFIX(Z_runPostSetsZ_vv))(void);
/* export: '_flag_enc' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__flag_encZ_i));
/* export: '_k' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__kZ_i));
/* export: '_r' */
extern u32 (*WASM_RT_ADD_PREFIX(Z__rZ_i));
#ifdef __cplusplus
}
#endif

#endif  /* EASYWASM_H_GENERATED_ */
