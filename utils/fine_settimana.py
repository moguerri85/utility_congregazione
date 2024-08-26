from bs4 import BeautifulSoup

def combine_html_fine_settimana(html1, html2):
    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')
    html1 = soup1.find_all("div", {"class": "d-flex flex-wrap align-self-start flex-grow-1"})
    html2 = soup2.find_all("div", {"class": "card"})

    # html2 i div card sono duplicati, utilizzare solo quelli con indice pari 0,2,4,6....
    html2 = [v for i, v in enumerate(html2) if i % 2 == 0]

    html_content = manipulateHTML_fine_settimana(html1, html2)
    return html_content

def manipulateHTML_fine_settimana(discorsoFS, programmaFS):
    countProFs = 0        
    for htmlProFS in programmaFS:  # array di 1
        isSpeciale = False
        discProFS = None  # Inizializza discProFS come None
        
        for buttonProFS in htmlProFS.find_all('button'):  # alcuni bottoni hanno i nominativi
            buttonProFS.replace_with(buttonProFS.text)     
        
        for row in htmlProFS.find_all("div", class_="col-12 col-lg-4 mb-3 p-0"):       
            for item in row.find_all("label", class_="fw-bolder text-muted mb-1 form-label"):
                if "Preghiera iniziale" in item.text:
                    row.extract()
                if "Preghiera conclusiva" in item.text:
                    row.extract()    
                if "Conduttore Studio Torre di Guardia" in item.text:
                    row.extract()
                if "Lettore S.T.d.G." in item.text:
                    for item1 in row.find_all("div", class_="dropdown-bounded dropdown"):
                        if "Nessuna selezione" in item1.text:
                            row.extract()                   
            
        for row1 in htmlProFS.find_all("div", class_="row mx-0 px-0 mb-3 justify-content-between"):
            for item1 in row1.find_all("div", class_="col-12 col-lg-4 pb-3 d-flex p-0"):
                for canticoInzProFS in item1.find_all("div", class_="ms-2"):    
                    canticoInzProFS.extract()
            if "Presidente" in row1.text:
                for item2 in row1.find_all("div", class_="dropdown-bounded dropdown"):
                    if "Nessuna selezione" in item2.text:
                        row1.extract()   

        # in caso di congresso di zona
        for row2 in htmlProFS.find_all("span", class_="ms-1 badge text-dark bg-light"):
            if "Congresso di zona" in row2.text:
                row2.extract()
            if "Assemblea di circoscrizione" in row2.text:
                row2.extract()
            
        isNessunDiscorso = False
        for discProFS in htmlProFS.find_all("div", class_="row px-0 mx-0 pt-3 pb-3 border-top"):                       
            for discorsoFS_dett in discorsoFS:
                for buttonDisFS in discorsoFS_dett.find_all('button'):
                    buttonDisFS.extract()  # modifica aggiungi copia sezione discorsi
                    
                    for copiaFS in discorsoFS_dett.find_all("div", class_="dropdown btn-group btn-group-sm"):                        
                        copiaFS.extract()

                    for discFS in discorsoFS_dett.find_all("p", class_="mb-3"):
                        if "Nessun discorso in programma" in discFS.text:
                            discFS.extract()
                        
                    for row3 in discorsoFS_dett.find_all("span", class_="ms-1 badge text-dark bg-light"):
                        valoreRow3 = row3.text                            
                        if "Congresso di zona" in valoreRow3:    
                            isSpeciale = True
                            row3.clear()
                            row3.replace_with(BeautifulSoup("<div class='special d-flex'><h4 class='fw-bolder'>"+valoreRow3+"</h4></div>", 'html.parser'))
                        elif "Assemblea di circoscrizione" in valoreRow3:
                            isSpeciale = True
                            row3.clear()                                                      
                            row3.replace_with(BeautifulSoup("<div class='special d-flex'><h4 class='fw-bolder'>"+valoreRow3+"</h4></div>", 'html.parser'))
                        else:
                            isSpeciale = False
                                                         
                    for rowDiscFS in discorsoFS_dett.find_all("h5", class_="d-flex align-items-center fw-bolder mb-4"):
                        rowDiscFS.name = "h6"  # converto h5 in h6 dei discorsi
                    for rowDisc1FS in discorsoFS_dett.find_all("span", class_="ms-1 badge text-dark bg-light"):
                        rowDisc1FS.name = "h6"  # converto badge in h6
                    for rowOratoreFS in discorsoFS_dett.find_all("h4", class_="fw-bold mb-0 me-2"):    
                        rowOratoreFS.name = "h6"  # converto h4 in h6 dei oratori
                    for rowOratoreFSAcc in discorsoFS_dett.find_all("span", class_="mx-1 d-flex gap-1"):
                        rowOratoreFSAcc.extract()

        # Controlla se è un evento speciale
        if "Congresso di zona" in discorsoFS[countProFs].text:    
            isSpeciale = True
        elif "Assemblea di circoscrizione" in discorsoFS[countProFs].text:
            isSpeciale = True
        else:
            isSpeciale = False
            
        # Verifica se discProFS è stato assegnato
        if discProFS is not None:
            if isSpeciale is False:                
                valueClass = "oratore_discorso"
            else:
                valueClass = "oratore_discorso_special"

            discProFS.replace_with(BeautifulSoup('<div class="'+valueClass+'"><div class="mx-3">'+str(discorsoFS[countProFs])+'</div></div>', 'html.parser'))
            
        countProFs += 1    
         
    string_html_content = "\n".join(str(x) for x in programmaFS)
    return string_html_content
