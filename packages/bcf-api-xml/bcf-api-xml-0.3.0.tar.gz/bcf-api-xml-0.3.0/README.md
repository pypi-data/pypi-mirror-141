BCF-API-XML-converter
=====================

BCF-API-XML-converter is a library to open BCFzip and get data similar to BCF API json and to save BCF API data as BCFzip files.

It exports BCF files in 2.1 format and converts files in versions 2.0 and 2.1 to BCF-API json 2.1.


# Install
```bash
pip install bcf-api-xml
```

# usage
```python
    from bcf_api_xml import to_zip, to_json

    file_like_bcf_zip = to_zip(topics, comments, viewpoints)

    imported_topics = to_json(file_like_bcf_zip)
```

# develop
```bash
poetry shell
poetry install
pytest
pre-commit install
```

# Publish new version
```bash
poetry publish --build --username= --password=
```
