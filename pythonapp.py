
import db
import appdbcityneo4j
from geopy.geocoders import Nominatim
from gmplot import gmplot
import os
import webbrowser
from googlesearch import search

def menu():
    print("**********************************")
    print("             MENU                 ")
    print("1. View Cities by Country")
    print("2. Update City population")
    print("3. Add New Person")
    print("4. Delete Person")
    print("5. View Countries by population")
    print("6. Show Twinned Cities")
    print("7. Twin with Dublin")
    print("8. Co-ordinates of any City")
    print("9. Find City on Google Maps")
    print("10. Google Search")
    print("x. Exit the application")
    print("**********************************")

def get_choice():
    return input ("Choice :")

def main():
    menu()
    while True:
        try:
            choice = get_choice()
            if choice == "1":
                print("View Cities by Country")
                print("-------------------")
                get_cities()
                print()
            elif choice == "2":
                print("Update City population")
                print("-------------------")
                update_pop()
                print()
            elif choice == "3":
                print("Add New Person")
                print("-------------------")
                add_newperson()
                print()
            elif choice == "4":
                print("Delete Person")
                print("-------------------")
                delete_person()
                print()
            elif choice == "5":
                countries_by_pop()
                print()
            elif choice == "6":
                print("Show Twinned Cities")
                print("-------------------")
                show_twinned()
                print()
            elif choice == "7":
                print("Twin with Dublin")
                print("-------------------")
                twin_dublin()
                print()
            elif choice == "8":
                print("Innovation. Co-ordinates of any City")
                coordinates()
            elif choice == "9":
                print("Innovation.Find City on Google Maps")
                find_city()
            elif choice == "10":
                print("Innovation. Google Search")
                search_google()
            elif choice == "x":
                print("Exit application")
                return
            else :
                print("Invalid choice. Try again")
        except pymysql.err.ProgrammingError as e:
            print("Programming error", e)
            menu()
        except pymysql.err.Error as e:
            print("Database connection already closed ", e)
            menu()
        except pymysql.err.IntegrityError as e:
            print("Integrity Error ", e)
            menu()
        except Exception as e:
            print("Error", e)
            menu()
        menu()

def get_cities():
    country = input ("Enter Country Name :")
    country_wild = '%'+country+'%'  
    cities = db.get_cities(country_wild)
    counter=0
    for city in cities:
        print("Country :", city["CountryName"], "| " "City Name : ", city["CityName"], "| ", "District Name : ", city["District"],"| ", "City Population : ",city["Population"] )
        counter +=1
        if counter%2 == 0:
            quit = input ("-- To Quit press (q). To see more press any other key --")
            if quit == "q":
                return

def countries_by_pop():
    print("View Countries by population")
    symbol = input ("Enter < > or = : ")
    while True:
        if symbol == "<":
            pop = enter_pop()
            pop_less = db.pop_less(pop)
            for country in pop_less:
                print("Code :", country["Name"], "| ", "Name : ", country["Name"], "| ","Continent : ", country["Continent"], "| ",  "Population : ",country["Population"] )
            return
        elif symbol == ">":
            pop = enter_pop()
            pop_more = db.pop_more(pop)
            for country in pop_more:
                print("Code :", country["Name"], "| ", "Name : ", country["Name"], "| ","Continent : ", country["Continent"], "| ",  "Population : ",country["Population"] )
            return
        elif symbol == "=":
            pop = enter_pop()
            pop_equal = db.pop_equal(pop)
            for country in pop_equal:
                print("Code :", country["Name"], "| ", "Name : ", country["Name"], "| ","Continent : ", country["Continent"], "| ",  "Population : ",country["Population"] )
            return
        else:
            symbol = input ("Invalid. Enter < > or = : ")
    
def enter_number():
    while True:
        num = input("Please enter a valid number : ")
        try:
            val = int(num)
            break;  
        except ValueError:
            print("This is not a number. Try again.")
        except:
            print("This is not a number. Try again")
    return val
             
def enter_pop():
    while True:
        num = input("Please enter population : ")
        try:
            val = int(num)
            break;  
        except ValueError:
            print("This is not a number. Try again.")
        except:
            print("This is not a number. Try again")
    return val

def enter_id():
    while True:
        id = input ("Enter City ID : ")
        try:
            val = int(id)
            #return val
            break;
        except ValueError:
            print("This is not a number. Try again")
        except:
            print("This is not a number. Try again")
    return val               

def update_pop():
    while True:
        id = input ("Enter City ID : ")
        try:
            check_city = db.check_city(id)
            if check_city == ():
                print("City ID "+id+" doesn't exist. Try again" )
            else:
                break
        except:
            break
    db.select_pop(id)
    incdec = input ("[I]ncrease/[D]ecrease Population :] ")
    while True:
        try:
            if incdec == "I":
                pop = enter_pop()
                break
            elif incdec == "D":
                pop = enter_pop()
                break
            else:
                incdec = input ("Invalid Entry. Try again.[I]ncrease/[D]ecrease Population :] ")
        except pymysql.err.DataError as e:
            print("Data Error", e) 
        except:
            print("Miscellaneous Error", e)
    db.update_pop(pop, id)
    db.select_pop(id)

def add_newperson():
    while True:
        try:
            add_ID = input ("ID :")
            check_id = db.check_id(add_ID)
            if check_id != ():
                print("Error: Person ID " +add_ID+ " already exists.")
                return
            add_Name = input ("Name :")
            add_Age = int(input ("Age :"))
            add_Salary = input ("Salary :")
            add_City = input ("City ID :")
            check_city = db.check_city(add_City)
            if check_city == ():
                print("Error: City ID "+add_City+" does not exist." )
                return
            db.add_person(add_ID, add_Name, add_Age, add_Salary, add_City)
            break            
        except Exception as e:
            print("There was an Error. ", e)
            return


def delete_person():
    while True:
        try:
            ID = input ("Enter ID of Person to Delete :")
            check_id = db.check_id(ID)
            if check_id == (): 
                print("Error. Cannot delete Person ID " +ID+ ". He/she doesn't exist.")
                print("Please try another Person ID.")
            else:
                break
        except Exception as e:
            print("There was an Error. ", e)
            return 
    try:
        hasvisitedcities = db.hasvisitedcities(ID)
        if hasvisitedcities == ():
           db.delete_person(ID) 
           print("Person ID " +ID+ " deleted" )
        else: 
          print("Error. Cannot delete Person ID " +ID+ ". He/she has visited cities.")
          return
    except Exception as e:
        print("Error. ", e)

def show_twinned():
    cities = appdbcityneo4j.print_twins()
    city = cities[0]
    for city in city:
            print(city[0],"<->", city[1])

def twin_dublin():
    cid = input ("Enter ID of City to twin with Dublin :")
    while True:
        try:
            check_city = db.check_city(cid)
            name = check_city[0]
            print("You wish to twin "+name["Name"]+" with Dublin.")
            print("Please wait a few seconds while we process your request.")
            name = name["Name"]
            if check_city == ():
                print("City ID " +cid+ " doesn't exist in MySQL database. Try again" )
                cid = input ("Enter City ID to twin with Dublin: ")
            elif name == "Dublin":
               print("Error: Dublin can not be twinned with Dublin. Try a different City ID.")
               cid = input ("Enter City ID to twin with Dublin: ") 
            else:
                break
        except Exception as e:
            print("City ID " +cid+ " doesn't exist in MySQL database. Try again. ", e)
            cid = input ("Enter City ID to twin with Dublin: ")
    check_id = appdbcityneo4j.check_id(cid)
    check_twins = appdbcityneo4j.check_twins(cid)
    if check_id.records == []:
        appdbcityneo4j.create_twin(cid,name)
        appdbcityneo4j.twin(cid)
        print(name+ " is now twinned with Dublin.")
    elif check_twins.records == []:
        appdbcityneo4j.twin(cid)
        print(name+ " is now twinned with Dublin.")
    else:
        print(name+ " was already twinned with Dublin.")
        return

def coordinates():
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")

    loc = input("Please enter City name: ") 
    location = geolocator.geocode(loc)
    lat = location.latitude
    long = location.longitude

    print("The latitude of "+loc+ " is: ", location.latitude)
    print("The longitude of "+loc+ " is: ", location.longitude)

    db.update_latlong(lat,long,loc)

    print("Database updated with coordinates of "+loc)

def find_city():
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")

    loc = input("please enter City name: ") 
    location = geolocator.geocode(loc)
    lat = location.latitude
    long = location.longitude

    gmap = gmplot.GoogleMapPlotter(lat, long, 10)

    # Add a marker
    gmap.marker(lat, long, 'cornflowerblue')

    # Draw map into HTML file
    gmap.draw("my_map.html")

    filename = 'file:///'+os.getcwd()+'/' + 'my_map.html'
    webbrowser.open_new_tab(filename)

    #db.update_latlong(lat,long,loc)
    #print("The database was updated with the coordinates of "+loc)

def search_google():
    query = input('Please enter Search query: ')
    for url in search(query, stop=10):
        print (url)
        print()
    return
          
if __name__ == "__main__":
    main()