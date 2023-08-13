def run():
    #!/usr/bin/env python
    # coding: utf-8

    # In[167]:


    import pandas as pd
    import datetime as dt
    import math

    pd.set_option('display.max_columns', None) #parametro para apresentar colunas ocultas do dataframe


    # In[168]:


    df1 = pd.read_csv('data/1_azul.csv')
    df2 = pd.read_csv('data/2_amarela.csv')
    df3 = pd.read_csv('data/3_rosa.csv')
    df4 = pd.read_csv('data/4_verde.csv')
    df5 = pd.read_csv('data/5_vermelha.csv')
    df6 = pd.read_csv('data/6_laranja.csv')


    # Converter as horas dos Dataframes que estão em formato String para Time

    # In[169]:


    # alterando tipo de dados para data no dataframe 1
    for column in df1.columns[:-1]:
        # Convert the Time column to datatime format
        df1[column] = pd.to_datetime(df1[column], format='%H:%M').dt.time
        '''.dt é um acessador (accessor) no pandas que permite acessar
        várias propriedades de um objeto datetime. O .time é uma dessas
        propriedades, que retorna o componente de tempo do objeto datetime.'''

    # alterando tipo de dados para data no dataframe 2
    for column in df2.columns[:-1]:
        # Convert the Time column to datatime format
        df2[column] = pd.to_datetime(df2[column], format='%H:%M').dt.time

    # alterando tipo de dados para data no dataframe 3
    for column in df3.columns[:-1]:
        # Convert the Time column to datatime format
        df3[column] = pd.to_datetime(df3[column], format='%H:%M').dt.time

    # alterando tipo de dados para data no dataframe 4
    for column in df4.columns[:-1]:
        # Convert the Time column to datatime format
        df4[column] = pd.to_datetime(df4[column], format='%H:%M').dt.time

    # alterando tipo de dados para data no dataframe 5
    for column in df5.columns[:-2]:
        # Convert the Time column to datatime format
        df5[column] = pd.to_datetime(df5[column], format='%H:%M').dt.time

    # alterando tipo de dados para data no dataframe 6
    for column in df6.columns[:-2]:
        # Convert the Time column to datatime format
        df6[column] = pd.to_datetime(df6[column], format='%H:%M').dt.time



    # In[170]:


    #Verificar se estamos em periodo escolar para apagar os hoários do periodo não letivo e vice e versa.

    # Obter o ano atual
    ano_atual = dt.datetime.now().year

    # Definir os períodos escolares com o ano vigente
    periodo_escolar_inicio = dt.date(ano_atual, 9, 1)
    periodo_escolar_fim = dt.date(ano_atual, 6, 30)

    # Obtenha a data atual
    data_atual = dt.datetime.now().date()

    # Verifique se a data atual está dentro do período
    periodo_escolar = periodo_escolar_inicio <= data_atual <= periodo_escolar_fim

    if periodo_escolar:
        resposta = 'Sim'
    else:
        resposta = 'Não'

    # Imprima o resultado
    print(f"A data atual está dentro do período: {periodo_escolar} ({resposta})")


    # In[171]:


    # Filtrar os dataframes que tenham horarios deferentes em periodos letivos com vase na checagem a cima

    # Verificar o valor da variável e apagar a linha correspondente
    if periodo_escolar:
        # Apagar linha onde 'periodo_escolar' é igual a 0
        df6 = df6[df6['periodo_escolar'] != 0]
        df5 = df5[df5['periodo_escolar'] != 0]
    else:
        # Apagar linha onde 'periodo_escolar' é igual a 1
        df6 = df6[df6['periodo_escolar'] != 1]
        df5 = df5[df5['periodo_escolar'] != 1]



    # Forma de calcular a diferença entre datas.
    #
    # foi adicionado a data atual a hora, pq não é possível, segundo pesquisas, calcular a diferença somente entre horas...
    # sendo necessário combinar alguma data, no caso, a data atual (datetime.today()).

    # Para encontrar a menor diferença de tempo entre uma coluna de horas em um DataFrame pandas e a hora atual, você pode seguir os seguintes passos:

    # In[172]:


    # CLASSE HoraAutocarro()

    class HoraAutocarro:
        def __init__(self, nome_paragem, nome_rota):
            self.nome_paragem = nome_paragem
            self.nome_rota = nome_rota

        def ProximoAutocarro(self):
            #verificar se existe a paragem para determinada linha
            if self.nome_paragem not in self.nome_rota.columns:
                return 'Não constam dados nesta linha sobre esta paragem.'

            #Parametros de tempo do metodo:
            hora_atual = dt.datetime.now()


            #Dataframes filtrados:
            #Filtragem dos valores NAN, caso existam.
            if self.nome_rota[self.nome_paragem].isna().any():
                df_filtrado1 = self.nome_rota[~self.nome_rota[self.nome_paragem].isna()]
                df_filtrado = df_filtrado1[df_filtrado1[self.nome_paragem] >= hora_atual.time()]
            else:
                df_filtrado = self.nome_rota[self.nome_rota[self.nome_paragem] >= hora_atual.time()]

            # Filtrando a última hora da série com base no dia da semana.
            if hora_atual.weekday() < 5: #hj é dia da semana!
                df_week = df_filtrado.query('sabado  == 0')
                ultima_hora = df_week[self.nome_paragem].tolist()


            else:
                df_weekend = df_filtrado.query('sabado  == 1') #hj é sábado!
                ultima_hora = df_weekend[self.nome_paragem].tolist()



            #Verificação de saidas para as variações de tempo e dados de entrada

            #Verificar o dia da semana para filtrar a base de dados
            if hora_atual.weekday() == 6: #hj é domingo!
                return "Não existem autocarros para o dia de hoje!"

            elif hora_atual.weekday() == 5: #hj é sábado!
                df_sabado = self.nome_rota[~self.nome_rota[self.nome_paragem].isna()].query('sabado  == 1')
                if df_sabado.shape[0] == 0:
                    return "Segundo a tabela de horários, aos sábados não constam autocarros para esta linha."

                elif len(ultima_hora) == 0:
                    return "Segundo a tabela de horários, o último autocarro já passou por esta paragem."

                else:
                    # Df com os valores para sábado, excluindo as linhas com as horas inferios a hora atual
                    df_sabado_filtrado = df_filtrado.query('sabado  == 1')

                    # Calcular a diferença de tempo entre cada valor na coluna de horários da paragem e a hora atual
                    df_sabado_filtrado['diferenca'] = df_sabado_filtrado[self.nome_paragem].apply(lambda x: dt.datetime.combine(dt.datetime.today(), x) - dt.datetime.combine(dt.datetime.today(), hora_atual.time()))

                    # Encontrar o índice da hora mais próxima
                    indice_hora_proxima = df_sabado_filtrado['diferenca'].idxmin()

                    # Obter a hora mais próxima
                    hora_proxima = df_sabado_filtrado.loc[indice_hora_proxima, self.nome_paragem]

                    #Retorno do proximo autocarro"
                    return f"{hora_proxima.hour:02d}:{hora_proxima.minute:02d}"


            elif hora_atual.weekday() < 5: #hj é dia da semana!
                if len(ultima_hora) == 0:
                    return "Segundo a tabela de horários, o último autocarro já passou por esta paragem."

                else:
                    df_semana = df_filtrado.query('sabado  == 0')

                    # Calcular a diferença de tempo entre cada valor na coluna de horários da paragem e a hora atual
                    df_semana['diferenca'] = df_semana[self.nome_paragem].apply(lambda x: dt.datetime.combine(dt.datetime.today(), x) - dt.datetime.combine(dt.datetime.today(), hora_atual.time()))

                    # Encontrar o índice da hora mais próxima
                    indice_hora_proxima = df_semana['diferenca'].idxmin()

                    # Obter a hora mais próxima
                    hora_proxima = df_semana.loc[indice_hora_proxima, self.nome_paragem]


                    #Retorno do proximo autocarro"
                    return f"{hora_proxima.hour:02d}:{hora_proxima.minute:02d}"



        def TempoEspera(self):
            #verificar se existe a paragem para determinada linha
            if self.nome_paragem not in self.nome_rota.columns:
                return ""
                #return 'Não constam dados nesta linha sobre esta paragem'

            #Parametros de tempo do metodo:
            hora_atual = dt.datetime.now()

            #Dataframes filtrados:
            #Filtragem dos valores NAN, caso existam e filtragem (retirada do df) das horas inferiores a hora atual.

            if self.nome_rota[self.nome_paragem].isna().any():
                df_filtrado = self.nome_rota[~self.nome_rota[self.nome_paragem].isna()]
                df_filtrado = df_filtrado[df_filtrado[self.nome_paragem] >= hora_atual.time()]

            else:
                df_filtrado = self.nome_rota[self.nome_rota[self.nome_paragem] >= hora_atual.time()]



            # Filtrando a última hora da série com base no dia da semana.
            if hora_atual.weekday() < 5: #hj é dia da semana!
                df_week = df_filtrado.query('sabado  == 0')
                ultima_hora = df_week[self.nome_paragem].tolist()


            else:
                df_weekend = df_filtrado.query('sabado  == 1') #hj é sábado!
                ultima_hora = df_weekend[self.nome_paragem].tolist()


            #Verificação de saidas para as variações de tempo e dados de entrada

            #Verificar o dia da semana para filtrar a base de dados
            if hora_atual.weekday() == 6: #hj é domingo!
                return ""
                #return "Não existem autocarros para o dia de hoje!"

            elif hora_atual.weekday() == 5: #hj é sábado!
                df_sabado = self.nome_rota[~self.nome_rota[self.nome_paragem].isna()].query('sabado  == 1') #df_sabado = df_filtrado.query('sabado  == 1')
                if df_sabado.shape[0] == 0:
                    return ""
                    #return "Segundo a tabela de horários, aos sábados não constam autocarros para esta paragem."

                elif len(ultima_hora) == 0: #hora_atual.time() > ultima_hora[-1]: verificar se o último autocarro já passou pela paragem
                    return ""
                    #return "Segundo a tabela de horários,  o último autocarro já passou por esta paragem."

                else:
                    # Df com os valores para sábado, excluindo as linhas com as horas inferios a hora atual com base no df_filtrado e retirando da analise os valores NAN
                    df_sabado_filtrado = df_filtrado.query('sabado  == 1')

                    # Calcular a diferença de tempo entre cada valor na coluna de horários da paragem e a hora atual
                    df_sabado_filtrado['diferenca'] = df_sabado_filtrado[self.nome_paragem].apply(lambda x: dt.datetime.combine(dt.datetime.today(), x) - dt.datetime.combine(dt.datetime.today(), hora_atual.time()))

                    # Encontrar a menor diferença de tempo
                    menor_diferenca = df_sabado_filtrado['diferenca'].min()


                    hora= int(menor_diferenca.total_seconds() // 3600)
                    minuto = int((menor_diferenca.total_seconds() // 60) % 60)

                    #Retorno do tempo de espera"
                    return f"{hora:02d}:{minuto:02d}min."


            elif hora_atual.weekday() < 5: #hj é dia da semana!
                if len(ultima_hora) == 0:
                    return ""

                else:
                    df_semana = df_filtrado.query('sabado  == 0')


                    # Calcular a diferença de tempo entre cada valor na coluna de horários da paragem e a hora atual
                    df_semana['diferenca'] = df_semana[self.nome_paragem].apply(lambda x: dt.datetime.combine(dt.datetime.today(), x) - dt.datetime.combine(dt.datetime.today(), hora_atual.time()))

                    # Encontrar a menor diferença de tempo
                    menor_diferenca = df_semana['diferenca'].min()

                    hora= int(menor_diferenca.total_seconds() // 3600)
                    minuto = int((menor_diferenca.total_seconds() // 60) % 60)

                    #Retorno do tempo de espera"
                    return f"{hora:02d}:{minuto:02d}min."







    # #Testes para criar uma formatação do POPUP
    #
    #
    # def FormatTexto(hora_autocarro, tempo_espera):
    #     if hora_autocarro == "Não constam dados nesta linha sobre esta paragem":
    #         pass
    #     else:
    #         return hora_autocarro + tempo_espera

    # In[173]:


    def TextoFormatado(nome_autocarro, tempo_espera,linha):

        if linha is df1:
            texto_linha = 'L1 - Azul'
        elif linha is df2:
            texto_linha = 'L2 - Amarela'
        elif linha is df3:
            texto_linha = 'L3 - Rosa'
        elif linha is df4:
            texto_linha = 'L4 - Verde'
        elif linha is df5:
            texto_linha = 'L5 - Vermelha'
        elif linha is df6:
            texto_linha = 'L6 - Laranja'


        texto_formatado1 = f'<br><br><strong>{texto_linha}:</strong> {nome_autocarro} <strong>({tempo_espera})</strong>'
        texto_formatado2 = f'<br><br><strong>{texto_linha}:</strong> {nome_autocarro}'

        #texto_formatado1 = f'{texto_linha}: {nome_autocarro} ({tempo_espera})'
        #texto_formatado2 = f'{texto_linha}: {nome_autocarro}'

        if nome_autocarro == 'Não constam dados nesta linha sobre esta paragem.':
            pass
        elif nome_autocarro == 'Não existem autocarros para o dia de hoje!':
            return texto_formatado2
        elif nome_autocarro == 'Segundo a tabela de horários, aos sábados não constam autocarros para esta linha.':
            return texto_formatado2
        elif nome_autocarro == 'Segundo a tabela de horários, o último autocarro já passou por esta paragem.':
            return texto_formatado2
        else:
            return texto_formatado1


     #"<br><br><strong>L1 - Azul:</strong> " + autocarro_df1.ProximoAutocarro() + " <strong>(" + autocarro_df1.TempoEspera() + ")</strong>"


    # Visualizar os dados em um mapa Folium
    #

    # In[174]:


    import folium
    from folium.plugins import LocateControl
    from folium.plugins import MarkerCluster
    import geopandas as gpd
    from shapely import Point

    paragem = gpd.read_file("./shp/paragem_autocarro_lamego.shp")
    linhas = gpd.read_file("./shp/rota_autocarro.shp")

    tabela_horarios = "https://www.transdev.pt/sites/default/files/pdf-sim/verdinho_info_site_1801.pdf"

    linha_amarela = linhas.query("linha == 'amarela'")
    linha_azul = linhas.query("linha == 'azul'")
    linha_rosa = linhas.query("linha == 'rosa'")
    linha_verde = linhas.query("linha == 'verde'")
    linha_vermelha = linhas.query("linha == 'vermelha'")
    linha_laranja = linhas.query("linha == 'laranja'")

    m = folium.Map(#width=600, height=600,
               location=[paragem.geometry.y.mean(), paragem.geometry.x.mean()],
               zoom_start=14,
               )


    url_logo_lamego = "https://cdn1.omeuwebsite.com/users/nervir/other/lamego.jpg"
    link_url = "https://www.cm-lamego.pt/"

    m.get_root().html.add_child(folium.Element(f"""
    <div style="position: fixed; right: 20px; bottom: 20px; width: 100px; height: 100px; z-index: 900;">
        <a href="{link_url}" target="_blank">
            <img src="{url_logo_lamego}" alt="Minha Imagem" width="100" height="100">
        </a>
    </div>
    """
    ))

    LocateControl(auto_start= True,
                  strings={"title": "See you current location",
                  "popup": "Sua localização aprox."}
                  ).add_to(m)

    #add novo basemap
    #folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(m)
    #folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(m)
    '''folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
           ).add_to(m)'''

    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                     attr='Google Satellite',
                     name='Google Satélite',
                     overlay=False).add_to(m)

    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
                     attr='Google Satellite with Labels',
                     name='Google Satélite com rótulos',
                     overlay=False
                     ).add_to(m)

    # grupo de layers

    shapesparegem = folium.FeatureGroup(name= 'Paragem').add_to(m) # MARCADOR NORMAL (SEM EFEITOS)

    #shapesparegem = MarkerCluster(name= 'Paragem').add_to(m) # MARCADOR CLUSTER

    '''folium.GeoJson(
        paragem,
        popup= 'teste',
        zoom_on_click=True, #centraliza a pag no ponto clicado
        style_function=lambda feature: {
            'fillColor': 'green',
            'color': 'darkred',
            'weight': 0.1,
            'icon': 'bus'
        }
    ).add_to(m)'''

    #shape de paragens
    for id in range(paragem.shape[0]):
        #hora_autocarro_df1 = HoraAutocarro(paragem['nome'][id],df1)
        autocarro_df1 = HoraAutocarro(paragem['nome'][id],df1)
        autocarro_df2 = HoraAutocarro(paragem['nome'][id],df2)
        autocarro_df3 = HoraAutocarro(paragem['nome'][id],df3)
        autocarro_df4 = HoraAutocarro(paragem['nome'][id],df4)
        autocarro_df5 = HoraAutocarro(paragem['nome'][id],df5)
        autocarro_df6 = HoraAutocarro(paragem['nome'][id],df6)

        texto1= TextoFormatado(autocarro_df1.ProximoAutocarro(),autocarro_df1.TempoEspera(),df1)
        texto2= TextoFormatado(autocarro_df2.ProximoAutocarro(),autocarro_df2.TempoEspera(),df2)
        texto3= TextoFormatado(autocarro_df3.ProximoAutocarro(),autocarro_df3.TempoEspera(),df3)
        texto4= TextoFormatado(autocarro_df4.ProximoAutocarro(),autocarro_df4.TempoEspera(),df4)
        texto5= TextoFormatado(autocarro_df5.ProximoAutocarro(),autocarro_df5.TempoEspera(),df5)
        texto6= TextoFormatado(autocarro_df6.ProximoAutocarro(),autocarro_df6.TempoEspera(),df6)

        texto_completo = f"{texto1 if texto1 else ''} \n  {texto2 if texto2 else ''} \n  {texto3 if texto3 else ''} \n  {texto4 if texto4 else ''} \n  {texto5 if texto5 else ''} \n  {texto6 if texto6 else ''}"


        link_google_maps = 'http://www.google.com/maps/place/'+ str(paragem['lat'][id]) + ',' + str(paragem['long'][id])
        location = [paragem['geometry'][id].y, paragem['geometry'][id].x]
        icon = folium.features.CustomIcon("static\images\icon_bus.png", icon_size=(20,20))
        popup = folium.Popup("<strong>Tempo de espera:</strong>" +
                              texto_completo +
                            "<br><br>Período escolar: <strong>"+ resposta +"</strong></a>"
                            "<br>Link Google Maps (localização): <a href='" + link_google_maps + "' target='_blank'>link</a> <br>" +
                            "Link Tabela de Horários Verdinho (Transdev): <a href='" + tabela_horarios + "' target='_blank'>link</a>",

            max_width=580
        )

        marker= folium.Marker(
            location=location,
            popup=popup,
            tooltip='<strong>'+ str(paragem['nome'][id]) + '</strong>',
            icon=icon

        ).add_to(shapesparegem)




    # Função para definir o estilo com base em um atributo
    def style_function(feature):
        color = '#000000'  # Cor padrão (preto)

        # Obter o valor do atributo desejado
        attribute_value = feature['properties']['linha']

        # Definir a cor com base no valor do atributo
        if attribute_value == 'amarela':
            color = '#F9C900'  # amarela
        elif attribute_value == 'verde':
            color = '#BFD611'  # Verde
        elif attribute_value == 'azul':
            color = '#38A2E6'  # azul
        elif attribute_value == 'rosa':
            color = '#E3008D'  # rosa
        elif attribute_value == 'vermelha':
            color = '#E41619'  # vermelha
        elif attribute_value == 'laranja':
            color = '#EB7806'  # laranja
        # Adicione mais condições if/elif conforme necessário para mapear outros valores do atributo

        return {'color': color, 'weight': 2}  # Retornar um dicionário de estilo com a cor e a espessura da linha


    # Adicionar as linhas ao mapa com o estilo definido pela função style_function
    folium.GeoJson(linha_azul, style_function=style_function, name='Linha 1 -  Azul', show=False,tooltip='Linha 1').add_to(m)
    folium.GeoJson(linha_amarela, style_function=style_function, name='Linha 2 -  Amarela', show=False,tooltip='Linha 2').add_to(m)
    folium.GeoJson(linha_rosa, style_function=style_function, name='Linha 3 -  Rosa', show=False,tooltip='Linha 3').add_to(m)
    folium.GeoJson(linha_verde, style_function=style_function, name='Linha 4 -  Verde', show=False,tooltip='Linha 4').add_to(m)
    folium.GeoJson(linha_vermelha, style_function=style_function, name='Linha 5 -  Vermelha', show=False,tooltip='Linha 4').add_to(m)
    folium.GeoJson(linha_laranja, style_function=style_function, name='Linha 6 -  Laranja', show=False,tooltip='Linha 5').add_to(m)



    folium.LayerControl().add_to(m)

    m.save('templates/Mapa - Autocarros de Lamego - PT.html')

print('execução do codigo!')

