#include <iostream>
#include <librsvg/rsvg.h>

int main() {
    RsvgHandle* handle = rsvg_handle_new();
    rsvg_handle_close(handle, NULL);
}
