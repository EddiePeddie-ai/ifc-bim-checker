#!/usr/bin/env python3
import json
import os

def main():
    # read report.json if exists
    if not os.path.exists('report.json'):
        print('report.json not found')
        return
    with open('report.json','r',encoding='utf-8') as f:
        try:
            report = json.load(f)
        except Exception:
            report = []
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "IFC BIM Checker",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }
    # write empty sarif
    with open('report.sarif','w',encoding='utf-8') as f:
        json.dump(sarif,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    main()
