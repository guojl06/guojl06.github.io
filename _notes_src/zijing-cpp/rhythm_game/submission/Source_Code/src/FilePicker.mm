#include <string>

#ifdef __APPLE__
#include <AppKit/AppKit.h>

std::string openAudioFileDialog() {
    @autoreleasepool {
        NSOpenPanel* panel = [NSOpenPanel openPanel];
        [panel setTitle:@"Select Audio File"];
        [panel setCanChooseFiles:YES];
        [panel setCanChooseDirectories:NO];
        [panel setAllowsMultipleSelection:NO];
        [panel setAllowedFileTypes:@[@"mp3", @"wav", @"ogg", @"flac", @"m4a", @"aac"]];

        if ([panel runModal] == NSModalResponseOK) {
            NSURL* url = [[panel URLs] objectAtIndex:0];
            return std::string([url fileSystemRepresentation]);
        }
        return "";
    }
}
#else
#include <cstdio>
std::string openAudioFileDialog() {
    char buf[1024];
    printf("Enter audio file path: ");
    if (fgets(buf, sizeof(buf), stdin)) {
        std::string s = buf;
        while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
        return s;
    }
    return "";
}
#endif
