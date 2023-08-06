from boto3.dynamodb.conditions import Key

Secret_Key="Ilvoqrt"

def clean_projection(projection,data):
    res=projection.split(',')
    main_values=list()
    dist_values=list()
    dist_names=list()
    for ele in res:
        if is_dictionary_property(ele):
            res=ele.split('.')
            dist_values.append(res[0])
            dist_values.append(res[1])
        elif is_dictionary(ele,data):
            dist_names.append(ele)
        else:
            main_values.append(ele)
    return main_values,dist_values,dist_names
def is_dictionary_property(projection):
    if projection.find(".")>0:
        return True
    return False
def is_dictionary(projection,data):
    if type(data[projection]) is dict:
        return True
    return False
def is_list(data,name):
    if name.find(".")>0:
        res=name.split(".")
        if type(data[res[0]].get(res[1])) is list:
            return True
    return False
def has_sort_key(client,tablename):
    response = client.describe_table(TableName=tablename)
    response=response['Table']
    response=response['KeySchema']
    if len(response)==2:
        return True
    return False

def filter_details_helper_query(tablename,queriesnames,queriesvalues,data,client):
        attributenames={}
        attributevalues={}
        keyexpression=""
        filterexpression=""
        naming1=queriesnames[0].replace(".","")
        keyexpression+='#'+naming1+' = :'+naming1+' and '
        attributenames['#'+naming1]=queriesnames[0]
        attributevalues[':'+naming1]=queriesvalues[0]
        for i in range(1,len(queriesnames)):
            naming1=queriesnames[i].replace(".","")
            if is_list(data,queriesnames[i]):
                filterexpression+='contains('+queriesnames[i]+', :'+naming1+') and '
                attributevalues[':'+naming1]=queriesvalues[i]
            else:
                filterexpression+=queriesnames[i]+' = :'+naming1+' and '
                attributevalues[':'+naming1]=queriesvalues[i]
        return keyexpression,filterexpression,attributenames,attributevalues

def filter_details_helper_scan(queriesnames,queriesvalues,data):
        attributevalues={}
        filterexpression=""
        for i in range(0,len(queriesnames)):
            naming1=queriesnames[i].replace(".","")
            if is_list(data,queriesnames[i]):
                filterexpression+='contains('+queriesnames[i]+', :'+naming1+') and '
                attributevalues[':'+naming1]=queriesvalues[i]
            else:
                filterexpression+=queriesnames[i]+' = :'+naming1+' and '
                attributevalues[':'+naming1]=queriesvalues[i]
        return filterexpression,attributevalues
