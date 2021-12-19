# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
import cufflinks
import ipywidgets as widgets
from IPython.display import display, clear_output

# Data cleaning

# Creating dataframes
tags = pd.read_csv("tags.csv")
torrents = pd.read_csv("torrents.csv")

# Changing columns names
tags.rename(columns={"index": "Index", "id": "ID", "tag": "Tag"}, inplace=True)
torrents.rename(columns={"groupName": "Release Name", "totalSnatched": "Total Snatched", "artist": "Artist", 
                        "groupYear": "Release Year", "releaseType": "Release Type", "groupId": "Group ID",
                        "id": "ID"}, inplace=True)

# Converting into title format
tags["Tag"] = tags["Tag"].str.title()
torrents["Release Name"] = torrents["Release Name"].str.title()
torrents["Artist"] = torrents["Artist"].str.title()
torrents["Release Type"] = torrents["Release Type"].str.title()

# Replacing wrong characters
tags["Tag"] = tags["Tag"].str.replace(".", " ")
tags["Tag"] = tags["Tag"].str.replace("S$", "s", regex = True)
torrents["Release Name"] = torrents["Release Name"].str.replace("&#39;", "'")
torrents["Release Name"] = torrents["Release Name"].str.replace("&Amp;", "&")
torrents["Release Name"] = torrents["Release Name"].str.replace("&Quot;", "\"")
torrents["Release Name"] = torrents["Release Name"].str.replace("&Aacute;", "á")
torrents["Artist"] = torrents["Artist"].str.replace("&#39;", "'")
torrents["Artist"] = torrents["Artist"].str.replace("&Amp;", "&")
torrents["Artist"] = torrents["Artist"].str.replace("&Quot;", "\"")
torrents["Artist"] = torrents["Artist"].str.replace("&Aacute;", "á")

# Checking for NaNs in tags dataframe
is_NaN_tags = tags.isnull()
row_has_NaN_tags = is_NaN_tags.any(axis=1)
rows_with_NaN_tags = tags[row_has_NaN_tags]

# Checking for NaNs in torrents dataframe
is_NaN_torrents = torrents.isnull()
row_has_NaN_torrents = is_NaN_torrents.any(axis=1)
rows_with_NaN_torrents = torrents[row_has_NaN_torrents]

# Removing NaNs and reset indexes
tags = tags.dropna().reset_index(drop=True)
torrents = torrents.dropna().reset_index(drop=True)

# Checking for duplicates
torrents[torrents.duplicated(subset="ID")]

# Main function
def main():
    print("""
    Co słychać w Zatoce Piratów?\n
    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀⠀⠀
⠀⠀⠀⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    
    """)
    button_value_counts_1.on_click(value_counts_eventhandler_1)
    display(button_value_counts_1)
    button_value_counts_2.on_click(value_counts_eventhandler_2)
    display(button_value_counts_2)
    button_value_counts_3.on_click(value_counts_eventhandler_3)
    display(button_value_counts_3)
    display(out)

# Buttons

# First button function
def value_counts_eventhandler_1(obj):
    with out:
        clear_output()
        print("""
        Baza danych pobrana z serwisu What.CD.\n\
        Zawiera dane o torrentach z płytami otagowanymi jako \"Hip-Hop\"\n\
        Łącznie składa się z 75 719 wpisów według stanu na 22.10.2016 r.""")

# Second button function
def value_counts_eventhandler_2(obj):
    with out:
        clear_output()
        show_widget_stat()

# Third button function
def value_counts_eventhandler_3(obj):
    with out:
        clear_output()
        show_widget_visual()

# Buttons info
button_value_counts_1 = widgets.Button(description='Wprowadzenie')
button_value_counts_2 = widgets.Button(description='Statystyka')
button_value_counts_3 = widgets.Button(description='Wizualizacje')

# Buttons output
out = widgets.Output()

# Statistic functions

# Statistic widget function
def show_widget_stat():
    display(my_choice_widget_stat, handler_out_stat)

# Statistic choice function
def my_choice_handler_stat(widget_value):
    if widget_value == "...":
        print("Wybierz interesujące Cię zestawienie.")
    elif widget_value == "Najczęściej pobierani artyści":
        artist_rank()
    elif widget_value == "Najczęściej pobierane rodzaje wydawnictw":
        year_release_rank()
    elif widget_value == "Liczba pobranych wydawnictw":
        year_snatched_rank()
    elif widget_value == "Najpopularniejsze tagi":
        year_tags_rank()
    elif widget_value == "Najczęśćiej pobierane płyty z danego roku":
        year_toptitle_rank()
        
my_choice_widget_stat = widgets.Dropdown(options=["...", \
                                             "Liczba pobranych wydawnictw", \
                                             "Najczęściej pobierani artyści", \
                                             "Najczęściej pobierane rodzaje wydawnictw", \
                                             "Najczęśćiej pobierane płyty z danego roku", \
                                             "Najpopularniejsze tagi"])
handler_out_stat = widgets.interactive_output(my_choice_handler_stat, \
                                              {"widget_value": my_choice_widget_stat})

# Statistic minor functions

# Artist / snatched rank function
def artist_rank():
    label_artist_rank = widgets.Label("Podana wartość musi być liczbą naturalną mniejszą lub równą 50.")
    text_artist_rank = widgets.Text()
    
    def text_submitted_artist_rank(widget_value_artist_rank):
        if widget_value_artist_rank.isdigit() == False or int(widget_value_artist_rank) \
        <= 0 or int(widget_value_artist_rank) > 50:
            label_artist_rank.layout.visibility = "visible"
            display(label_artist_rank)
        else:
            label_artist_rank.layout.visibility = "hidden"
            x_artist_rank = int(widget_value_artist_rank)
            artist_rank_df = torrents[["Artist","Total Snatched"]]
            artist_rank_df = artist_rank_df.groupby(by="Artist")
            artist_rank_df = artist_rank_df.sum()
            print(artist_rank_df.sort_values("Total Snatched",ascending=False)[:x_artist_rank])
            
    print("Wybierz, ilu artystów chcesz zobaczyć:")
    handler_out_artist_rank = widgets.interactive_output(text_submitted_artist_rank, \
                                                         {"widget_value_artist_rank": text_artist_rank})
    text_artist_rank.on_submit(text_submitted_artist_rank)
    display(text_artist_rank, handler_out_artist_rank)   
    label_artist_rank.layout.visibility = "hidden"

# Year / release rank function
def year_release_rank():
    label_year_release_rank = widgets.Label("Tylko dane dla lat 1979-2016.")
    text_year_release_rank = widgets.Text()
    
    def text_submitted_year_release_rank(widget_value_year_release_rank):
        if widget_value_year_release_rank.isdigit() == False or \
        int(widget_value_year_release_rank) < 1979 or int(widget_value_year_release_rank) > 2016:
            label_year_release_rank.layout.visibility = "visible"
            display(label_year_release_rank)
        else:
            label_year_release_rank.layout.visibility = "hidden"
            x_year_release_rank = int(widget_value_year_release_rank)
            year_type_df = torrents[torrents["Release Year"] == x_year_release_rank]
            year_type_df = year_type_df["Release Type"].value_counts()
            print(year_type_df)
            
    print("Wybierz, z którego roku podać dane: ")
    handler_out_year_release_rank = widgets.interactive_output(text_submitted_year_release_rank, \
                                                               {"widget_value_year_release_rank": \
                                                                text_year_release_rank})
    text_year_release_rank.on_submit(text_submitted_year_release_rank)
    display(text_year_release_rank, handler_out_year_release_rank)
    label_year_release_rank.layout.visibility = "hidden"

# Year / snatched rank function
def year_snatched_rank():
    label_year_snatched_rank = widgets.Label("Tylko dane dla lat 1979-2016.")
    text_year_snatched_rank = widgets.Text()
    
    def text_submitted_year_snatched_rank(widget_value_year_snatched_rank):
        if widget_value_year_snatched_rank.isdigit() == False or int(widget_value_year_snatched_rank) \
        < 1979 or int(widget_value_year_snatched_rank) > 2016:
            label_year_snatched_rank.layout.visibility = "visible"
            display(label_year_snatched_rank)
        else:
            label_year_snatched_rank.layout.visibility = "hidden"
            x_year_snatched_rank = int(widget_value_year_snatched_rank)
            year_snatched_df = torrents[torrents["Release Year"] == x_year_snatched_rank]
            year_snatched_df = year_snatched_df["Total Snatched"].sum()
            print(f"Pobrano łącznie {year_snatched_df} płyt wydanych w {x_year_snatched_rank} roku.")
    
    print("Wybierz, z którego roku podać wydawnictwa: ")
    handler_out_year_snatched_rank = widgets.interactive_output(text_submitted_year_snatched_rank, \
                                                                {"widget_value_year_snatched_rank": \
                                                                 text_year_snatched_rank})
    text_year_snatched_rank.on_submit(text_submitted_year_snatched_rank)
    display(text_year_snatched_rank, handler_out_year_snatched_rank)
    label_year_snatched_rank.layout.visibility = "hidden"

# Year / tags rank function
def year_tags_rank():
    label_year_tags_rank = widgets.Label("Tylko dane dla lat 1979-2016.")
    text_year_tags_rank = widgets.Text()
    
    def text_submitted_year_tags_rank(widget_value_year_tags_rank):
        if widget_value_year_tags_rank.isdigit() == False or int(widget_value_year_tags_rank) \
        < 1979 or int(widget_value_year_tags_rank) > 2016:
            label_year_tags_rank.layout.visibility = "visible"
            display(label_year_tags_rank)
        else:
            label_year_tags_rank.layout.visibility = "hidden"
            x_year_tags_rank = int(widget_value_year_tags_rank)
            tags_year_df = pd.merge(tags, torrents[["ID","Release Year"]],on="ID", how="left")
            tags_year_df = tags_year_df[tags_year_df["Release Year"] == x_year_tags_rank]
            tags_year_df = tags_year_df["Tag"].value_counts().head(50)
            print(tags_year_df)
            
    print("Wybierz, z którego roku podać dane: ")
    handler_out_year_tags_rank = widgets.interactive_output(text_submitted_year_tags_rank, \
                                                            {"widget_value_year_tags_rank": \
                                                             text_year_tags_rank})
    text_year_tags_rank.on_submit(text_submitted_year_tags_rank)
    display(text_year_tags_rank, handler_out_year_tags_rank)
    label_year_tags_rank.layout.visibility = "hidden"

# Year / toptitle rank function
def year_toptitle_rank():
    label_year = widgets.Label("Tylko dane dla lat 1979-2016.")
    label_title_count = widgets.Label("Podana wartość musi być liczbą mniejszą lub równą 50.")
    text_year = widgets.Text()
    text_title_count = widgets.Text()
    
    def text_submitted_year_toptitle_rank(str_year, str_title_count):
        year = 0
        title_count = 0
        if str_year.isdigit() == False or int(str_year) < 1979 or int(str_year) > 2016:
            year = 0
            if str_year != "":
                label_year.layout.visibility = "visible"
            else:
                label_year.layout.visibility = "hidden"
        else:
            label_year.layout.visibility = "hidden"
            year = int(str_year)
        
        if str_title_count.isdigit() == False or int(str_title_count) <= 0 or int(str_title_count) > 50:
            title_count = 0
            if str_title_count != "":
                label_title_count.layout.visibility = "visible"
            else:
                label_title_count.layout.visibility = "hidden"
        else:
            label_title_count.layout.visibility = "hidden"
            title_count = int(str_title_count)
        
        show_results_year_toptitle_rank(year, title_count)
        
    def show_results_year_toptitle_rank(year, title_count):
        if year >= 1979 and year <= 2016 and title_count > 0 and title_count <= 50:
            year_toptitle_df = torrents.where(torrents["Release Year"] == year)
            year_toptitle_df = year_toptitle_df[["Release Name","Total Snatched"]]
            year_toptitle_df = year_toptitle_df.groupby(by="Release Name")
            year_toptitle_df = year_toptitle_df.sum()
            year_toptitle_df = year_toptitle_df.sort_values\
            ("Total Snatched",ascending=False)[:title_count]
            print(f"Dla {year} roku ranking wygląda następująco: {year_toptitle_df} ")
        else:
            print("")
        
    print("Wybierz, z którego roku podać dane: ")
    text_year.on_submit(text_submitted_year_toptitle_rank)
    display(text_year, label_year)
    
    print("Wybierz, ile najczęściej pobieranych płyt chcesz zobaczyć: ")
    text_title_count.on_submit(text_submitted_year_toptitle_rank)
    display(text_title_count, label_title_count)
    
    handler_out_year_toptitle_rank = widgets.interactive_output(text_submitted_year_toptitle_rank, \
                                                                {"str_year": text_year, \
                                                                 "str_title_count": text_title_count})
    display(handler_out_year_toptitle_rank)
    label_year.layout.visibility = "hidden"
    label_title_count.layout.visibility = "hidden"

# Visual functions

# Visual widget function
def show_widget_visual():
    display(my_choice_widget_visual, handler_out_visual)
    
# Visual choice function
def my_choice_handler_visual(widget_value):
    if widget_value == "...":
        print("Wybierz interesującą Cię wizualizację.")
    elif widget_value == "Wizualizacje dotyczące zestawienia lat":
        plt.subplot(121)
        torrents["Release Year"].plot(kind = 'box', vert = False, figsize = (14,6))
        plt.subplot(122)
        torrents["Release Year"].plot(kind = 'density', figsize = (14,6))
        plt.show()
    elif widget_value == "Najpopularniejsze rodzaje wydawnictw":
        releases_df = torrents["Release Type"].value_counts().head(10)
        releases_df.plot(kind = "pie", figsize =(14,6))
    elif widget_value == "Top 10 najczęściej pobieranych płyt":
        albums_df = torrents[["Release Name", "Total Snatched"]]
        albums_df = albums_df.groupby(by="Release Name")
        albums_df = albums_df.sum()
        albums_df = albums_df.sort_values("Total Snatched",ascending=False)[:10]
        albums_df.plot(kind = "pie", figsize =(14,8),subplots=True)
    elif widget_value == "Trendy rodzajów wydawnictw na przestrzeni lat":
        show_widget_type_per_year()
    elif widget_value == "Trendy tagów na przestrzeni lat":
        show_widget_tags_per_year()
        
my_choice_widget_visual = widgets.Dropdown(options=["...", \
                                                    "Wizualizacje dotyczące zestawienia lat", 
                                                    "Najpopularniejsze rodzaje wydawnictw", \
                                                    "Trendy rodzajów wydawnictw na przestrzeni lat", \
                                                    "Top 10 najczęściej pobieranych płyt", \
                                                    "Trendy tagów na przestrzeni lat"])
handler_out_visual = widgets.interactive_output(my_choice_handler_visual, \
                                                {"widget_value": my_choice_widget_visual})

# Visual minor functions

# Release type / year function
def show_widget_type_per_year():
    display(my_choice_widget_type_per_year, handler_out_type_per_year)

def my_choice_handler_type_per_year(widget_value):
    if widget_value == "...":
        print("Wybierz interesującą Cię kategorię.")
    elif widget_value == "Album":
        type_per_year_df = torrents[torrents["Release Type"] == "Album"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')        
    elif widget_value == "Single":
        type_per_year_df = torrents[torrents["Release Type"] == "Single"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Ep":
        type_per_year_df = torrents[torrents["Release Type"] == "Ep"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Compilation":
        type_per_year_df = torrents[torrents["Release Type"] == "Compilation"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Mixtape":
        type_per_year_df = torrents[torrents["Release Type"] == "Mixtape"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Remix":
        type_per_year_df = torrents[torrents["Release Type"] == "Remix"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Anthology":
        type_per_year_df = torrents[torrents["Release Type"] == "Anthology"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Dj Mix":
        type_per_year_df = torrents[torrents["Release Type"] == "Dj Mix"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Bootleg":
        type_per_year_df = torrents[torrents["Release Type"] == "Bootleg"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Soundtrack":
        type_per_year_df = torrents[torrents["Release Type"] == "Soundtrack"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')
    elif widget_value == "Live Album":
        type_per_year_df = torrents[torrents["Release Type"] == "Live Album"]
        type_per_year_df = type_per_year_df[["Release Type","Release Year"]]
        type_per_year_df.plot.hist(bins = 30, align='right', color='green', edgecolor='black')

my_choice_widget_type_per_year = widgets.Dropdown(options=["...",\
                                                          "Album",\
                                                          "Single",\
                                                          "Ep",\
                                                          "Compilation",\
                                                          "Mixtape",\
                                                          "Remix",\
                                                          "Anthology",\
                                                          "Dj Mix",\
                                                          "Bootleg",\
                                                          "Soundtrack",\
                                                          "Live Album"])
handler_out_type_per_year = widgets.interactive_output(my_choice_handler_type_per_year, \
                                              {"widget_value": my_choice_widget_type_per_year})

# Tags / year function

def show_widget_tags_per_year():
    display(my_choice_widget_tags_per_year, handler_out_tags_per_year)

def my_choice_handler_tags_per_year(widget_value):
    if widget_value == "...":
        print("Wybierz interesującą Cię kategorię.")
    elif widget_value == "Electronic":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Electronic"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 35, align='right', color='blue', edgecolor='black')
    elif widget_value == "2020s":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "2020s"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 5, align='right', color='blue', edgecolor='black')
    elif widget_value == "Instrumental":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Instrumental"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Freely Available":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Freely Available"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 27, align='right', color='blue', edgecolor='black')
    elif widget_value == "Experimental":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Experimental"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "1990s":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "1990s"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Beats":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Beats"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Pop":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Pop"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "2000s":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "2000s"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Rhythm And Blues":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Rhythm And Blues"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Jazz":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Jazz"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Soul":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Soul"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Funk":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Funk"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Rock":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Rock"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Underground":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Underground"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Dance":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Dance"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
    elif widget_value == "Trap":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Trap"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 26, align='right', color='blue', edgecolor='black')
    elif widget_value == "Alternative":
        tags_per_year_df = pd.merge(torrents, tags, on="ID", how="left")
        tags_per_year_df = tags_per_year_df[tags_per_year_df["Tag"] == "Alternative"]
        tags_per_year_df = tags_per_year_df[["Tag","Release Year"]]
        tags_per_year_df.plot.hist(bins = 30, align='right', color='blue', edgecolor='black')
        
        
my_choice_widget_tags_per_year = widgets.Dropdown(options=["...",\
                                                          "Electronic",\
                                                          "2020s",\
                                                          "Instrumental",\
                                                          "Freely Available",\
                                                          "Experimental",\
                                                          "1990s",\
                                                          "Beats",\
                                                          "Pop",\
                                                          "2000s",\
                                                          "Rhythm And Blues",\
                                                          "Jazz",\
                                                          "Soul",\
                                                          "Funk",\
                                                          "Rock",\
                                                          "Underground",\
                                                          "Dance",\
                                                          "Trap",\
                                                          "Alternative"])
handler_out_tags_per_year = widgets.interactive_output(my_choice_handler_tags_per_year, \
                                              {"widget_value": my_choice_widget_tags_per_year})

main()