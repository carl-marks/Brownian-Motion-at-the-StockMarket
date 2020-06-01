```python
import bovespa
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
```


```python
cod_s=['BRFS3','SQIA3','CRFB3','IRBR3','WEGE3','MGLU3','RENT3','LREN3','ABEV3','ITSA4','PETR4','VALE3','JBSS3']
```


```python
years=['2019','2020']
```


```python
def year_writer(arg_cod,arg_year):
    for year in arg_year:
        year_data=pd.DataFrame()
        bf=bovespa.File('../RAW_DATAS/'+str(year)+'/COTAHIST_A'+str(year)+'.TXT')
        for cod in arg_cod:
            mean_price=[]
            for rec in bf.query(stock=str(cod)):
                mean_price.append(rec.price_mean)
            year_data[cod]=pd.Series(mean_price)
        year_data=year_data.dropna()
        year_data.to_csv('datas/anos/'+str(year)+'/all_share_mean_prices.csv',index=False)
```


```python
year_writer(cod_s,years)
```


```python
def var_year(arg_year):
    for year in arg_year:
        var_data=pd.read_csv('datas/anos/'+str(year)+'/all_share_mean_prices.csv')
        for col in var_data.columns:
            first_value=var_data[col][0]
            for index, rows in enumerate(var_data[col]):
                var_data.at[index,col]=rows-first_value
        var_data.to_csv('datas/anos/'+str(year)+'/all_share_variations.csv',index=False)
```


```python
var_year(years)
```


```python
def square_var_year(arg_year):
    for year in arg_year:
        sq_v_data=pd.read_csv('datas/anos/'+str(year)+'/all_share_variations.csv')
        for col in sq_v_data.columns:
            for index, row in enumerate(sq_v_data[col]):
                sq_v_data.at[index,col]=row**2
        sq_v_data['Mean']=sq_v_data.mean(axis=1)
        sq_v_data.to_csv('datas/anos/'+str(year)+'/all_square_variations.csv',mode='w',index=False)
```


```python
square_var_year(years)
```


```python
def grapher_year(arg_year):
    for year in arg_year:
        data=pd.read_csv('datas/anos/'+str(year)+'/all_square_variations.csv')
        x=data.index
        y=data['Mean']
        plt.xlabel('Time'); plt.ylabel('Mean Square Variation')
        plt.plot(x,y,label='mean square variation by time'); plt.legend(loc=0)
        plt.title(year); plt.savefig('datas/anos/'+str(year)+'/mean-square-variation.png')
        plt.show()
```


```python
grapher_year(years)
```


```python

```


```python
def month_writer(arg_cod,arg_year):
    for year in arg_year:
        bf=bovespa.File('../RAW_DATAS/'+str(year)+'/COTAHIST_A'+str(year)+'.TXT')
        for cod in arg_cod:
            share_data=pd.DataFrame()
            mean_price={}
            for rec in bf.query(stock=str(cod)):
                mean_price[rec.date]=rec.price_mean
            share_data['Date']=pd.to_datetime(list(mean_price.keys())) 
            #share_data['Date']=list(mean_price.keys())            
            #share_data['Date']=pd.to_datetime(share_data['Date'])
            months=[mon for mon in share_data['Date'].dt.month.unique()]
            share_data=share_data.set_index([share_data['Date'].dt.month])
            share_data['Mean_Price']=list(mean_price.values())            
            for mon in months:
                mon_data=pd.DataFrame()
                mon_data['Mean_Price']=list(share_data.loc[mon].Mean_Price)
                mon_data.to_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/'+str(cod)+'_prices.csv',index=False)
```


```python
month_writer(cod_s,years)
```


```python
def var_mon(arg_year,arg_cod):
    months=[m for m in range(1,13)]
    for year in arg_year:
        for mon in months:
            for cod in arg_cod:
                try:
                    var_data=pd.read_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/'+str(cod)+'_prices.csv')
                except:
                    continue
                else:
                    for col in var_data.columns:
                        first_value=var_data[col][0]
                        for index, rows in enumerate(var_data[col]):
                            var_data.at[index,col]=rows-first_value
                    var_data.to_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/'+str(cod)+'_variations.csv', index=False)
```


```python
var_mon(years,cod_s)
```


```python
def square_var_mon(arg_year,arg_cod):
    months=[m for m in range(1,13)]
    for year in arg_year:
        for mon in months:
            sq_v_data=pd.DataFrame()
            for cod in arg_cod:
                try:
                    s_var_data=pd.read_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/'+str(cod)+'_variations.csv')
                except:
                    continue
                else:
                    sq_v_data[cod]=s_var_data['Mean_Price']
            if len(sq_v_data.columns) > 0:
                for col in sq_v_data.columns:
                    for index, row in enumerate(sq_v_data[col]):
                        sq_v_data.at[index,col]=row**2
                sq_v_data['Mean']=sq_v_data.mean(axis=1)
                sq_v_data.to_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/square_variations.csv', index=False)
            else:
                continue
```


```python
square_var_mon(years,cod_s)
```


```python
def grapher_mon(arg_year):
    months=[m for m in range(1,13)]
    for year in arg_year:
        for mon in months:
            try:
                data=pd.read_csv('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/square_variations.csv')
            except:
                continue
            else:
                x=data.index; y=data['Mean']; l=str(mon)+'/'+str(year)
                plt.xlabel('Time'); plt.ylabel('Mean Square Variation')
                plt.plot(x,y,label='mean square variation by time'); plt.legend(loc=0)
                plt.title(l); plt.savefig('datas/anos/'+str(year)+'/meses/m_'+str(mon)+'/mean-square-variation.png')
                plt.show()
```


```python
grapher_mon(years)
```


```python

```
