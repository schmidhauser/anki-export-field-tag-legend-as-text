<style>
code {
    color: #d63384;
}
</style>

### Location, Marker, and Shortcuts

#### Location

`location.note_type` and `location.card_type` specify the note type and card type whose front template contains the legend.

#### Marker

The legend must be stored in an HTML comment containing the configured `marker`:

    <!--

    # FIELD AND TAG LEGEND

    [Legend goes here.]

    -->

The marker must occur exactly once in the configured front template. The comment delimiters `<!--` and `-->` and any leading or trailing whitespace are not included in the exported text.

The add-on only reads the template; it does not modify the template or any other part of the collection.

#### Shortcuts

`shortcut_save` sets the shortcut for **Save Field and Tag Legend as Text…** The default shortcut is `Meta+Ctrl+Shift+L` (`⌃⇧⌘L`); set it to `""` to disable it.

`shortcut_copy` sets the shortcut for **Copy Field and Tag Legend as Text**. It is disabled by default.

No restart is required.

On macOS, Qt interprets `Meta` as Control (`⌃`), `Ctrl` as Command (`⌘`), `Alt` as Option (`⌥`), and `Shift` as Shift (`⇧`).
