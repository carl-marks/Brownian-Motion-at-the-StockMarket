import bovespa

bf=bovespa.File('COTAHIST_A2020/COTAHIST_A2020.TXT')

cod_s=['BRFS3','SQIA3','CRFB3','IRBR3','WEGE3','MGLU3','RENT3','LREN3','PETR4']

for i in cod_s:
    with open('DATAS/2019/'+str(i)+'_data.csv','a+') as dt:
        dt.write('Data,Opening,Meaning,Closing\n')
        for rec in bf.query(stock=str(i)):
            dt.write('{},{},{},{} \n'.format(rec.date, rec.price_open, rec.price_mean, rec.price_close))