#python tool for color gradient
#additional code here https://bsou.io/posts/color-gradients-with-python

color_gradients =	{
  "standard": ['#40E0D0','#FF8C00','#FF0080'],
  "jshine": ['#12c2e9','#c471ed','#f64f59'],
  "magic": ['#5D26C1','#a17fe0','#59C173'],
  "atlas": ['#4BC0C8','#C779D0','#FEAC5E'],
  "hazel": ['#77A1D3','#79CBCA','#E684AE'],
  "bydesign": ['#009FFF','#ec2F4B'],
  "vicecity": ['#3494E6','#EC6EAD'],
  "timber": ['#fc00ff','#00dbde'],#violet blue
  "miaka": ['#0ABFBC','#FC354C'],
  "rea": ['#FFE000','#799F0C'],
  "green-red": ['00AB08', 'BB0103']
  #"martini": ['#FDFC47','#24FE41']#green yellow
}
def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]
def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])
def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}
#Use this functopm to obtain linear gradient between two colors
def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)
def concantenate_color_gradients(gradient_1, gradient_2):
  g1_hex = gradient_1['hex']

  g1_r = gradient_1['r']
  g1_g = gradient_1['g']
  g1_b = gradient_1['b']

  g2_hex = gradient_2['hex']
  g2_r = gradient_2['r']
  g2_g = gradient_2['g']
  g2_b = gradient_2['b']

  g1_hex.extend(g2_hex)
  g1_r.extend(g2_r)
  g1_g.extend(g2_g)
  g1_b.extend(g2_b)

  g = {'hex': g1_hex, 'r': g1_r, 'g': g1_g, 'b': g1_b}

  return g
def linear_gradient_triple(start_hex, middle_hex="#FFFFFF", finish_hex="#FFFFFF", n=10):
  n_even = n % 2 == 0
  n_half = n//2
  #if n is od the middle color have to be mixed
  if n_even:
    start_gradient = linear_gradient(start_hex, middle_hex, n_half + 1)
    #print(len(start_gradient) + 'start gradient')
    end_color_in_start_gradient = start_gradient['hex'][len(start_gradient) - 2]

    end_gradient = linear_gradient(middle_hex, finish_hex, n_half + 1)
    start_color_in_end_gradient = end_gradient['hex'][1]

    gradient_1 = linear_gradient(start_hex, end_color_in_start_gradient, n_half)
    gradient_2 = linear_gradient(start_color_in_end_gradient, finish_hex, n_half)

    g = concantenate_color_gradients(gradient_1, gradient_2)

    return g
  else:
    start_gradient = linear_gradient(start_hex, middle_hex, n_half + 1)
    end_gradient = linear_gradient(middle_hex, finish_hex, n_half + 1)

    hex_key = end_gradient['hex']
    r_key = end_gradient['r']
    g_key = end_gradient['g']
    b_key = end_gradient['b']

    del hex_key[0]
    del r_key[0]
    del g_key[0]
    del b_key[0]

    new_end_gradient = {'hex': hex_key, 'r': r_key, 'g': g_key, 'b': b_key, }

    g = concantenate_color_gradients(start_gradient, new_end_gradient)

    return g

#this function returns dictionary with hex codes
def get_color_gradient_dict(gradient = 'standard', n = 10):
  hex_set = color_gradients[gradient]
  colors = None
  if len(hex_set) == 2: colors = linear_gradient(hex_set[0], hex_set[1], n)
  elif len(hex_set) == 3: colors = linear_gradient_triple(hex_set[0], hex_set[1], hex_set[2], n)

  return colors

def get_color_gradient_array(gradient = 'standard', n = 10):
  return get_color_gradient_dict(gradient, n)['hex']