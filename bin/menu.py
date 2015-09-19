import datetime
import sys, math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib import cm
from notebook import Polynomial_Notebook, Zernike_Polynomial

class Menu:
  '''Display a menu and respond to choices when run.'''
  def __init__(self):
    self.notebook = Polynomial_Notebook()
    self.choices = {
      1: self.configure_notebook,
      2: self.add_polynomial,
      3: self.plot_polynomial,
      4: self.polynomial_comparison,
      5: self.quit
    }

  def display_menu(self):
    print("""
      Notebook Menu
      1. Configure Notebook
      2. Add Polynomial
      3. Plot Polynomial 
      4. Compare 2-D and 3-D plots
      5. Quit 
    """)

  def run(self):
    '''Display the menu and respond to choices.'''
    while True:
      self.display_menu()
      print "Polynomials in Notebook"
      print "-----------------------"
      polynomials = self.notebook.polynomials
      for polynomial in polynomials:
        print("{0}: created: {1} n,m: {2},{3} coeffs: {4}".format(
          polynomial.id, polynomial.creation_date, polynomial.n, polynomial.m, polynomial.coeffs))
      choice = input("Enter an option: ")
      action = self.choices.get(choice)
      if action:
        action()
      else:
        print("{0} is not a valid choice".format(choice))

  def configure_notebook(self):
    density = input("Enter a new plot density: ")
    self.density = density
    print("Density set to %d" % density)

  def add_polynomial(self):
    n = input("Enter an n value: ")
    m = input("Enter an m value: ")
    self.notebook.new_polynomial(n,m)
    print "Added a new polynomial."

  def plot_polynomial(self):
    poly_id = input("Enter the id for the polynomial to be plotted: ")
    save_plot = raw_input("Save plot (Y/N): ")
    show_plot = raw_input("Show plot (Y/N): ")
    if save_plot == 'Y': 
      image_title = raw_input("Enter the file name to be used: ")
      self.notebook.plot_polynomial(poly_id, save_plot, show_plot, image_title)
    else:
      self.notebook.plot_polynomial(poly_id, save_plot, show_plot)

  def polynomial_comparison(self):
    poly_id = input("Enter the id for the polynomial to be plotted: ")
    even_odd = raw_input("Plot (E)ven or (O)dd polynomial:")
    save_plot = raw_input("Save plot (Y/N): ")
    show_plot = raw_input("Show plot (Y/N): ")
    if save_plot == 'Y': 
      image_title = raw_input("Enter the file name to be used: ")
      self.notebook.polynomial_comparison(poly_id,even_odd, save_plot, show_plot, image_title)
    else:
      self.notebook.polynomial_comparison(poly_id,even_odd, save_plot, show_plot)
 
  def quit(self):
    print("Thank you for using your notebook today.")
    sys.exit(0)

if __name__ == "__main__":
  m = Menu()
  m.run()