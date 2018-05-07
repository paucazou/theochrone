# Theochrone

## What is Theochrone ?
Theochrone is a liturgical calendar for the Traditional Rite. You can enter a date, and it gives you the feasts for this date, with their class, liturgical time, colour, and much more. You can also search a feast by keywords. Many other options are available.

## Core Features
* The roman calendar of 1962, accessible by dates or by keywords. A range of dates, or a period (a week or a month, for instance), is also a good option to have a better look.
* **[NEW]** Twelve national propers: Australia, USA, Brazil, Canada, England, France, New Zealand, Poland, Portugal, Scotland, Spain and Wales.
* The calendar is connected to a website which provides the texts for the mass and the office of the feast.
* The Roman martyrology, used in 1962, accessible by date or by keywords.

## Interfaces
### Web
#### Website
The website provides you basic tools: search by date, by keywords and for a whole month. The Roman Martyrology is also available. See here : https://theochrone.fr
#### Widget
The Widget provides very limited infos, but can be a great feature on a website. For an example, see here : https://tradinews.blogspot.fr#theocontainer
#### Web Services
**Not yet available**

We want to create a Rest API to give you a complete control over the raw data. 
Why is it unaivalable now ? Web Services are really costly in term of resources. We need money to afford better servers. **We also haven't got enough time to make it** and we need help to create this API. Feel free to contribute.
### Graphical User Interface (GUI)
The Graphical User Interface (GUI) provides more infos. It is downloadable and can be used on **any** platform: Windows, macOS or Linux (even on BSD or some rarer OS).
### Command-line (CLI)
The command-line interface (CLI), available with every GUI, is the fastest and the most powerful way to use the Theochrone - but it is a bit rough for computer users not familiar with CLI. 
For more info, type in a terminal after downloading the program:
    theochrone --help

## Install from GitHub
1. Clone or download repository.
2. Open a console/terminal in the folder where you can find your clone/downloaded file.
3. Unzip it if necessary.
4. Install python3.5 or greater if it is not yet done. Please consult the documentation for your own OS and architecture on http://python.org/.
5. Enter following commands:
```shell
python pip -r requirements.txt # in many OSes, you should enter python3 instead of python, or python3.5
python pip -r dev_requirement.txt # only if you want to contribute to the project
msgfmt programme/i18n/fr_FR/LC_LANGUAGES/messages.po -o programme/i18n/fr_FR/LC_LANGUAGES/messages.mo # if you want to use CLI with french translation
python -c "import dataswitcher; dataswitcher.main(propers='all',ordo='1962')"
python -c "import dataswitcher; dataswitcher.xml_to_pkl('en_roman_martyrology');dataswitcher.xml_to_pkl('fr_roman_martyrology')" # if you want to use roman martyrology
lrelease programme/gui/i18n/theochrone.fr.ts # if you want to use the GUI with french translation
lrelease programme/gui/i18n/theochrone.en.ts # if you want to use the GUI with english translation
```
> Note that the version you download from Github may be broken. Feel free to contribute to fix the issue !


## Who are we ?
Unfortunately, 'we' are mainly one person : Philippe Aucazou, a young french catholic. However, many persons have helped us : do not hesitate to take a look at our THX.md file. You can also join us and contribute : we have **HUGE** needs in many domains, including programming, translating, and resources.
## Contribute
Maybe you can give us a little bit of help ? We need you in these domains:
* translations, especially in:
  * english
  * spanish
  * italian
  * portuguese

but any language is accepted, even Papuan language or Sindarin !
* programming, especially the **frontend** and the **GUI**
* researching resources, including:
  * pictures for every feast
  * local calendars (especially diocesan)
  * older versions of the martyrology
  * other latin rites, like Sarum, or the Mozarabic 

Do not hesitate to look at the **[issues](https://github.com/paucazou/theochrone/issues/)** ! 

We also like suggestions. Three important features have been suggested and are now implemented:
* the widget
* the Roman Martyrology 
* the export to calendars like Outlook, Google Calendar or iCal

**We really listen to your desires and requests, so feel free to suggest or ask us something new.**
## Languages and Frameworks
If you're interested in some form of collaboration, do not hesitate to have a look at this list. 
Also, this list may change one day, especially if you put forward something else.
* Core: *Python 3.5*
* Web
  * Backend: *Django 1.10*
  * Frontend: *Bootstrap 3*
    * HTML5/CSS3
    * Javascript with *jQuery*
* GUI: *PyQt5*
* Others:
  * Bash/Zsh
### Introducing other language
You want to contribute to Theochrone but you want to use your personal favorite language? You're welcome, *but...*
* if it is an interpreted language, like PHP, Perl, Ruby, be sure that it is worth to add a whole new interpreter ; your contribution must be very huge : a new important feature, at least. Indeed, imagine the weight of the program with two or more interpreters...
* if it is a compiled language, like C, Go, Rust, be sure that your module can be compiled on major architectures and OSes.
## Version
Latest version is 0.5.0
## New features available in v0.5.0
- [x] widget available in english.
  - [x] Rework ferial days names in english
- [x] CLI available in english: only for the current day on CLI. Keyword research is not available.
  - [x] rework translation full system
- [x] local propers :
  - [x] France;
  - [x] USA;
  - [x] England;
  - [x] Wales;
  - [x] Scotland;
  - [x] Canada;
  - [x] Brazil;
  - [x] Poland;
  - [x] Spain;
  - [x] Portugal;
  - [x] Australia;
  - [x] New Zealand;
- [x] local propers available on:
  - [x] website;
  - [x] widget;
  - [x] CLI;
    - [x] print proper name on screen if requested
  - [x] Gui;
- [x] update GUI to support new features.
- [x] export data to files:
  - [x] Formats:
    - [x] CSV;
    - [x] ICS;
  - [x] Availability:
    - [x] CLI;
    - [x] website;
    - [x] GUI;
- [ ] ~~a new convenient help app~~
- [ ] varia:
  - [x] enable twitter app in english
  - [x] add the rose colour into details of the third week of advent (optional liturgical colour)
  - [x] add proper in user preferences
