#!/usr/bin/env python
import sys
from termcolor import colored, cprint

def getPrintCondi(cond):
	if cond:
		return colored("[!]", "red", attrs=["reverse"])
	return colored("[+]", "blue", attrs=["reverse"])

def printError(msg: str):
	print(colored("[x]", "red", attrs=["reverse"]), colored(msg, "red"))


def printTitle(title: str):
	cprint("\n" + title, attrs=["bold", "underline"])


def printResult(title: str, data: dict):
	indent = "  "
	cprint("\n" + indent + title, "grey")

	for key, value in data.items():
		score, thres = value

		subtitle = colored(key, "grey", attrs=["bold"])
		print_score = None
		print_condi = True

		if type(thres) in [float, int]:
			print_condi = getPrintCondi(score > thres)
			print_score = colored(f"{score:.4f} / {thres:.4f}")
			if score > thres:
				print_score = colored(f"{score:.4f} / {thres:.4f}", "red")
				subtitle = colored(key, "red", attrs=["bold"])
			
		else:
			print_condi = getPrintCondi(score)
			print_score = colored("Yes" if score else "No", "red" if score else None)
			subtitle = colored(key, "red" if score else "grey", attrs=["bold"])


		print(
			indent * 2,
			subtitle.ljust(60, "."),
			print_condi,
			print_score,
		)
