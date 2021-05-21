import requests
import bs4
import csv
import os

# Scraping song list into csv with corresponding lyrics link
def build_csv():
    link = "https://www.malayalachalachithram.com/listsongs.php?tot=147&g=1414&p="
    with open("data/dataset.csv", "w") as ifile:
        writer = csv.writer(ifile)
        csv_arr = []
        for i in range(5):
            res = requests.get(link + str(i))
            noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
            table = noStarchSoup.findAll("table", {"class": "mdetails"})
            rows = next(iter(table))
            for row in rows:
                row_arr = []
                cells = row.findAll('td')
                if(not cells):
                    continue
                row_arr.append(cells[2].getText())
                for a in cells[1].find_all('a', href=True):
                    row_arr.append(a.getText()[:-4])
                    row_arr.append(
                        "https://www.malayalachalachithram.com/" + a['href'])
                csv_arr.append(row_arr)
        writer.writerows(csv_arr)
        ifile.close()

# Using links from csv to scrape each lyrics
def lyrics_scrap():
    with open("data/dataset.csv", "r") as ifile:
        reader = csv.reader(ifile)
        song_num=0
        links =[]
        for i,csv_row in enumerate(reader):
            if(csv_row[2] in links): continue
            else: links.append(csv_row[2])
            res = requests.get(csv_row[2])
            noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
            table = noStarchSoup.findAll("table", {"id": "tbllyrics"})
            rows = next(iter(table))
            row = next(iter(rows))
            cells = row.findAll('td')
            lyricsless = cells[0].findAll('script')
            # Ignoring lyricless results
            if(lyricsless):
                continue
            lyrics = (cells[0].getText())
            writer = (cells[0]).findAll('em')
            if writer : lyrics = lyrics.replace(next(iter(writer)).getText(),"")
            text_file = open("data/try/"+str(song_num)+".txt", "w")
            song_num+=1
            text_file.write(lyrics)
            text_file.close()


# Collecting Movie names that gave empty results while scraping lyrics
def missed_movies():
    with open("data/dataset.csv", "r") as ifile:
        reader = csv.reader(ifile)
        links =[]
        text_file = open("data/missed_movies.txt", "w")
        for i,csv_row in enumerate(reader):
            if(csv_row[2] in links): continue
            else: links.append(csv_row[2])
            res = requests.get(csv_row[2])
            noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
            table = noStarchSoup.findAll("table", {"id": "tbllyrics"})
            rows = next(iter(table))
            row = next(iter(rows))
            cells = row.findAll('td')
            lyricsless = cells[0].findAll('script')
            if(lyricsless):
                text_file.write(csv_row[0] +" "+ csv_row[1]+" lyrics \n")
                continue
        text_file.close()

            


if __name__ == "__main__":
    lyrics_scrap()
