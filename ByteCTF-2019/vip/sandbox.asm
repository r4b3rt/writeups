A = sys_number
A == open ? good : next
A == mprotect ? good : next
A == write ? good : next
A == read ? good : next
return ERRNO(0)
A == open ? good : next
A == exit ? good : next
return ERRNO(5)
good:
return ALLOW
bad:
return KILL
