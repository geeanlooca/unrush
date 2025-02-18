# unrush
A tool to scan a media library and set the default audio track to a preferred language


## Notes

- There can be cases in which the language of each track is undefined (Faster, Pussycat...)
- There can be cases in which no track is set as default
- Need to find a way to determine which language to set as default for cases above and for cases in which we don't know the original language (Perfect Days)

    - maybe set a preferential order? e.g.   *, "", "und", "italian", "en", *, "ru"?
        this would set the lowest priority to russian, then select whatever is left, but then pick english, followed by italian, and whatever else is there
        e.g. jap or kor for asian movies, maybe we prefer those in original language. 