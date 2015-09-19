import datetime
import sys, math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pyradi.ryplot as ryplot
from matplotlib import cm

last_id = 0

class Zernike_Polynomial:
  '''Represent a polynomial to be manipulated. 
  '''

  def __init__(self, m,n):
    '''Initialize a polynomial with m, n values.'''
    global last_id
    last_id += 1
    self.creation_date = datetime.date.today()
    self.m = m
    self.n = n
    self.id = last_id

    

  def zernike_Rcoeffs(self):
    '''
    Generate a list of coefficients for the polynomial
    Given an n and m generate a numpy array of n+1 elements which are 
    the coefficients of their indicial polynomial.
    '''
    m = self.m
    n = self.n

    self.coeffs = np.zeros(n+1)

    for k in range((n-m)/2+1):
        self.coeffs[n-2*k] = ((-1.)**k*math.factorial(n-k))/(math.factorial(k)*math.factorial((n+m)/2.-k)*math.factorial((n-m)/2.-k))

  def zernike_even(self,Rho,Theta,density):
    '''Generate the even polynomial
    Take as input n, m, Rho, and Theta, where [Rho,Theta] represents
    the mesh grid [0, 1] X [0, 2*pi]

    Create Z_even(Rho,Theta) a mesh-grid representing the multi-variate function on the domain.
    '''    
    self.Z_even = np.zeros((density,density))
    for k in range(self.coeffs.size):
        self.Z_even = self.Z_even + self.coeffs[k]*Rho**k*np.cos(self.m*Theta)    

    self
          
  def zernike_odd(self,Rho,Theta,density):
    '''Generate the odd polynomial
    Take as input n, m, Rho, and Theta, where [Rho,Theta] represents
    the mesh grid [0, 1] X [0, 2*pi]

    Create Z_odd(Rho,Theta) a mesh-grid representing the multi-variate function on the domain.
    '''   
    self.Z_odd = np.zeros((density,density))
    for k in range(self.coeffs.size):
        self.Z_odd = self.Z_odd + self.coeffs[k]*Rho**k*np.sin(self.m*Theta)    



class Polynomial_Notebook(object):
  """Initialize a notebook with an empty list."""
  def __init__(self):
    self.polynomials = []
    self.density = 100
    self.rho = np.linspace(0,1,self.density)
    self.theta = np.linspace(-math.pi,math.pi,self.density)
    self.Rho, self.Theta = np.meshgrid(self.rho,self.theta)
    self.X = self.Rho*np.cos(self.Theta)
    self.Y = self.Rho*np.sin(self.Theta)

  def new_polynomial(self,n,m):
    new_poly = Zernike_Polynomial(m,n)
    new_poly.zernike_Rcoeffs()
    new_poly.zernike_even(self.Rho,self.Theta,self.density)
    new_poly.zernike_odd(self.Rho,self.Theta,self.density)
    self.polynomials.append(new_poly)

  def _find_poly(self, poly_id):
    '''Locate the polynomial with the given id.'''
    for polynomial in self.polynomials:
      if str(polynomial.id) == str(poly_id):
        return polynomial
    return None

  def plot_polynomial(self,poly_id,save_plot, show_plot, image_title=None):
    poly = self._find_poly(poly_id)
    fig, (ax1,ax2) = plt.subplots(ncols=2,subplot_kw=dict(projection='polar'))
    ax1.pcolormesh(self.Theta, self.Rho, poly.Z_odd)
    ax1.set_title("Odd Polynomial")
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.pcolormesh(self.Theta, self.Rho, poly.Z_even)
    ax2.set_title("Even Polynomial")
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    fig.suptitle("Zernike Polynomial for $n =$ %d, $m =$ %d" % (poly.n,poly.m))
    if save_plot == 'Y':
      plt.savefig(image_title)
    if show_plot == 'Y':
      plt.show()

  def polynomial_comparison(self,poly_id,even_odd,save_plot, show_plot, image_title=None):

    poly = self._find_poly(poly_id)
    fig = plt.figure()
    if even_odd == 'E': 
      poly_to_plot = poly.Z_even
      plot_type = "Even"
    elif even_odd == 'O': 
      poly_to_plot = poly.Z_odd
      plot_type = "Odd"
    ax = fig.add_subplot(211,projection='polar')
    ax.pcolormesh(self.Theta, self.Rho, poly_to_plot)
    ax.set_title("%s Polynomial" % plot_type)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax = fig.add_subplot(212,projection='3d')
    ax.plot_surface(self.X,self.Y,poly_to_plot, rstride=1, cstride=1, cmap=cm.coolwarm)

    fig.suptitle("Zernike Polynomial for $n =$ %d, $m =$ %d" % (poly.n,poly.m))
    if save_plot == 'Y':
      plt.savefig(image_title)
    if show_plot == 'Y':
      plt.show()

if __name__ == "__main__":
  ortho = Zernike_Polynomial(4,2)
  