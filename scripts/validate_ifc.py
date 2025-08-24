#!/usr/bin/env python3
import json, os

def main():
    req_file = 'requirements.json'
    if not os.path.exists(req_file):
        print('requirements.json not found')
        return
    with open(req_file,'r',encoding='utf-8') as f:
        try:
            requirements = json.load(f)
        except Exception:
            requirements = []
    report = []
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        return
    for filename in os.listdir(downloads_dir):
        if filename.lower().endswith('.ifc'):
            for rule in requirements:
                entry = rule.copy()
                entry.update({'file': filename, 'status':'not_checked','total':0,'passed':0,'failed':0,'missing':0,'deviations':[]})
                report.append(entry)
    with open('report.json','w',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    with open('report.html','w',encoding='utf-8') as f:
        f.write('<html><body><h1>Validation not implemented</h1></body></html>')

if __name__ == '__main__':
    main()
