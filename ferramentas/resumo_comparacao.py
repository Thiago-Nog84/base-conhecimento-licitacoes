import csv,os
r=list(csv.DictReader(open('comparacao_conteudo_pdf_md.csv',encoding='utf-8-sig')))
same=0;diff=0
for x in r:
    if x['Classe']=='IGUAL':
        a=os.path.splitext(x['PDF'])[0].lower(); b=os.path.splitext(os.path.basename(x['MelhorMD']))[0].lower()
        if a==b: same+=1
        else: diff+=1
print('IGUAL com mesmo nome',same,'nome diferente',diff)
for c in ('IGUAL','PROVAVEL_REVISAR'):
    print('==',c)
    for x in [y for y in r if y['Classe']==c][:12]:
        print(x['Score'],'|',x['PDF'][:60],'->',os.path.basename(x['MelhorMD'])[:60])
