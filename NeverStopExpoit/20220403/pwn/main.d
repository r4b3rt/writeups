import std.stdio;
import std.format;
import std.range;
import std.typecons;
import std.algorithm;

// @safe ensures memory safety, yay!
// https://dlang.org/spec/memory-safe-d.html
@safe:

struct Array
{
private:
  long[] _arr; // List of long

public:
  this(ulong n) {
    if (n <= 2) 
      throw new Exception("Invalid number of arr");
    _arr = new long[n];
  }
  ~this() {}

  /* Set the position of a long */
  void set_long(ulong index, long v) {
    if (index > _arr.length - 1) // if _arr.length = 0, we can arbitrary write
      throw new Exception("Invalid index");

    _arr[index] = v;
  }
}


/* We need to wrap `readf` in a trusted function
   because it's @system and not thread safe */


long read_long(string msg) @trusted {
  long x;
  write(msg);
  readf("%d\n", x);
  return x;
}


ulong read_ul(string msg) @trusted {
  ulong i;
  write(msg);
  readf("%d\n", i);
  return i;
}

string read_str(string msg) @trusted {
  string s;
  write(msg);
  readf("%s\n", s);
  return s;
}

/* Create a new arr */
void arr_new(ref Array[string] ps) {
  string name = read_str("Name: ");

  ulong n = read_ul("Number of arr: ");

  Array p = Array(n);
  for (ulong i = 0; i < n; i++) {
    long v = read_long(format("arr[%d] = ", i));
    p.set_long(i, v);
  }

  ps[name] = p;
}


/* Rename a arr */
void arr_rename(ref Array[string] ps) {
  string old_name = read_str("(old) Name: ");
  string new_name = read_str("(new) Name: ");

  if (!(old_name in ps)) // Not found
    throw new Exception("No such arr: " ~ old_name);

  Array p;
  move(ps[old_name], p); // Make a copy

  if (new_name in ps) {
    // Ask when new name already exists
    writeln("Do you want to overwrite the existing arr?");
    writeln(new_name, " --> ", ps[new_name]); // for leak?

    string answer = read_str("[y/N]: ");
    if (answer[0] != 'Y' && answer[0] != 'y')
      return; // VUL: old_name not removed
  }

  // Remove original arr and move to target
  ps.remove(old_name);
  ps[new_name] = p;
}

/* Edit a long in a arr */
void arr_edit(ref Array[string] ps) {
  string name = read_str("Name: ");

  if (!(name in ps)) // Not found
    throw new Exception("No such arr: " ~ name);

  ulong index = read_ul("Index: ");
  long v = read_long(format("arr[%d] = ", index));
  ps[name].set_long(index, v);
}

/* Delete a arr */
void arr_delete(ref Array[string] ps) { // useless
  string name = read_str("Name: ");

  if (!(name in ps)) // Not found
    throw new Exception("No such arr: " ~ name);

  ps.remove(name);
}

/* Entry point! (@trusted for setvbuf) */
void main() @trusted
{
  Array[string] ps;

  stdin.setvbuf(0, _IONBF);
  stdout.setvbuf(0, _IONBF);

  writeln("1. New");
  writeln("2. Rename");
  writeln("3. Edit");
  writeln("4. Delete");

  while (true) {
    ulong choice;
    try {
      choice = read_ul("> ");
    } catch (Exception e) {
      break;
    }

    try {
      switch (choice) {
      case 1: arr_new(ps); break;
      case 2: arr_rename(ps); break;
      case 3: arr_edit(ps); break;
      case 4: arr_delete(ps); break;
      default: return;
      }
    } catch (Exception e) {
      writeln("[ERROR] ", e);
    }
  }
}
