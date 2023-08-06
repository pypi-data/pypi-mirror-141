# made by amin shahrabi 
# pygame_easy_btn
import pygame, sys

keyspressed = [pygame.QUIT, pygame.K_ESCAPE, pygame.K_q]
clicked = False
pygame.font.init()

def mainloop():
    global clicked
    '''need to be called in the game loop'''
    for event in pygame.event.get():
        if event.type in keyspressed:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

def exit_keys(keys_as_list = [pygame.QUIT, pygame.K_ESCAPE, pygame.K_q]):
    global keyspressed
    keyspressed = keys_as_list

def img_button_with_hover(surface, x_position, y_position, img_file, hover_img, transform_w = None, transform_h = None, clicked_function = "none"):
    '''button with hover'''
    global clicked
    img = pygame.image.load(img_file)
    hover_img = pygame.image.load(hover_img)
    if transform_w != None and transform_h != None:
        img = pygame.transform.smoothscale(img, (transform_w, transform_h))
        hover_img = pygame.transform.smoothscale(hover_img, (transform_w, transform_h))
    now_img = img
    rect = now_img.get_rect(center = (x_position, y_position))

    if rect.collidepoint(pygame.mouse.get_pos()):
        now_img = hover_img

    if clicked_function != "none":
        if clicked == True and rect.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False

    surface.blit(now_img, rect)
    
def img_button_without_hover(surface, x_position, y_position, img_file, transform_w = None, transform_h = None, clicked_function = "none"):
    '''button without hover'''
    global clicked
    img = pygame.image.load(img_file)
    if transform_w != None and transform_h != None:
        img = pygame.transform.smoothscale(img, (transform_w, transform_h))
    now_img = img
    rect = now_img.get_rect(center = (x_position, y_position))

    if clicked_function != "none":
        if clicked == True and rect.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False

    surface.blit(now_img, rect)

def shape_button_with_hover(surface , x_position, y_position , color, hover_color, width, height,  clicked_function = "none"):
    '''shape button with hover'''
    global clicked

    rectangle = pygame.Rect(x_position, y_position, width, height)

    if rectangle.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(surface, hover_color, rectangle)
    else:
        pygame.draw.rect(surface, color, rectangle)

    if clicked_function != "none":
        if clicked == True and rectangle.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False
   
def shape_button_without_hover(surface , x_position, y_position , color, width, height,  clicked_function = "none"):

    '''shape button without hover'''
    global clicked

    rectangle = pygame.Rect(x_position, y_position, width, height)

    if rectangle.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(surface, color, rectangle)
    else:
        pygame.draw.rect(surface, color, rectangle)

    if clicked_function != "none":
        if clicked == True and rectangle.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False

def text_button_with_hover(surface , text , x_position, y_position , color, hover_color,  font = pygame.font.Font(None, 40), clicked_function = "none") :
    '''shape button without hover'''
    global clicked

    text1 = font.render(text, True, color)
    text1_rect = text1.get_rect(center = (x_position, y_position))

    if text1_rect.collidepoint(pygame.mouse.get_pos()):
        text1 = font.render(text, True, hover_color)
    else:
        text1 = font.render(text, True, color)

    surface.blit(text1, text1_rect)
    if clicked_function != "none":
        if clicked == True and text1_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False

def text_button_without_hover(surface , text , x_position, y_position , color,  font = pygame.font.Font(None, 40), clicked_function = "none") :
    '''shape button without hover'''
    global clicked

    text1 = font.render(text, True, color)
    text1_rect = text1.get_rect(center = (x_position, y_position))

    if text1_rect.collidepoint(pygame.mouse.get_pos()):
        text1 = font.render(text, True, color)
    else:
        text1 = font.render(text, True, color)

    surface.blit(text1, text1_rect)
    if clicked_function != "none":
        if clicked == True and text1_rect.collidepoint(pygame.mouse.get_pos()):
            clicked_function()
            clicked = False