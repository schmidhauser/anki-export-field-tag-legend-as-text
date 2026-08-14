PACKAGE := ../anki-export-field-tag-legend-as-text.ankiaddon

FILES := \
	__init__.py \
	export_field_tag_legend_as_text.py \
	config.json \
	config.md \
	manifest.json \
	LICENSE

.PHONY: package clean

package:
	rm -f "$(PACKAGE)"
	zip -X -MM -T "$(PACKAGE)" $(FILES)
	unzip -l "$(PACKAGE)"

clean:
	rm -f "$(PACKAGE)"
