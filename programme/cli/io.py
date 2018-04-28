#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Handles input and output"""
import adjutoria
import argparse
import feastprinter
import messages


def firstUpper(words: str) -> str:
    """Uppercase the first character"""
    return words[0].upper() + words[1:]

### OUTPUT ###
def feast_results(args: argparse.Namespace,feast: adjutoria.Fete) -> str:
    """Return results which can be print on the screen.
    They are both readable and localized"""
    fw = feastprinter.FeastWrapper(feast,args.langue)
    verbose = args.verbose
    msg = messages.translated_messages('io',args.langue)
    sentence = ''

    # date
    if verbose:
        sentence += fw.fulldate + msg.colon
    elif args.date_affichee or args.INVERSE:
        sentence += fw.digitdate
        if args.jour_semaine:
            sentence += " ({})".format(fw.weekday)
        sentence += msg.colon
    elif args.jour_semaine:
        sentence += fw.weekday + msg.colon

    # name
    sentence += fw.name 

    # Pro Aliquibus Locis
    if feast.pal:
        sentence += " ({})".format(fw.pal)
    sentence += msg.dot

    # status
    if verbose or args.status:
        sentence += msg.status.format(fw.status)

    # class
    if (verbose or args.degre) and not feast.pal:
        sentence += fw.Class + msg.dot

    # transfert
    if (verbose or args.transfert) and feast.transferee:
        sentence += firstUpper(fw.transfert) + msg.dot

    # temporal/sanctoral
    if (verbose or args.temporal_ou_sanctoral) and not feast.pal:
        sentence += fw.temporsanct + msg.dot

    # liturgical season
    if verbose or args.temps_liturgique:
        sentence += fw.season + msg.dot

    # color
    if verbose or args.couleur:
        sentence += msg.color.format(fw.color)

    # station
    if (verbose or args.station) and fw.station:
        sentence += msg.station.format(fw.station)

    # proper
    if verbose or args.print_proper:
        sentence += msg.proper.format(fw.proper)

    # addendum
    if verbose:
        sentence += fw.addendum

    return sentence


def select_results(args: argparse.Namespace,feasts: list) -> str:
    """Select the results following the user
    request.
    feasts is a list of adjutoria.Fete."""
    results = ''
    for feast in feasts:
        if feast.omission and not args.verbose and not args.INVERSE or feast.pal and not args.pal:
            continue
        results += feast_results(args,feast) + '\n'

    return results



