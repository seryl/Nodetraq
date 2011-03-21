{
    "_id": "_design/dns",
    "language": "javascript",
    "views": {
        "configs" : {
            "map": "function(doc) {\n    if (doc.doc_type == \"dns\") {\n        emit(null, doc);\n    }\n}"
        }
    }
}
