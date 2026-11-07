from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
assert 'onedrive'not in str(ROOT).lower()
layout=(ROOT/'content/layout.html').read_text(encoding='utf-8')
pages=json.loads((ROOT/'content/pages.json').read_text(encoding='utf-8'))
for row in pages:
    path=row['path'];html=layout
    for token,value in {'TITLE':row['title'],'DESCRIPTION':row['description'],'PATH':''if path=='/'else path,'BODY':row['body']}.items():
        html=html.replace('{{'+token+'}}',value)
    if path!='/':html=html.replace('href="'+path+'">','href="'+path+'" aria-current="page">')
    target=ROOT/'public'/('index.html'if path=='/'else path.strip('/')+'/index.html')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8')
print('Built '+str(len(pages))+' pages.')
