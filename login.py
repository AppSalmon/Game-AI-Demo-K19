import pygame
from pygame.locals import *
def Login():
    pygame.init()

    data = {}
    window_width = 500
    window_height = 350
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Đăng nhập')
    pygame_icon = pygame.image.load('AiClub.jpg')
    pygame.display.set_icon(pygame_icon)
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (173, 216, 230)
    GRAY = (200, 200, 200)
    DARK_BLUE = (0, 32, 96)
    font = pygame.font.Font("Arial.ttf", 24)

    # Text inputs
    username = pygame.Rect(150, 100, 200, 32)
    email = pygame.Rect(150, 150, 200, 32)
    password = pygame.Rect(150, 200, 200, 32)

    # Input values
    username_value = ''
    email_value = ''
    password_value = ''

    # Submit button
    submit_button = pygame.Rect(150, 250, 100, 40)
    submit_label = font.render("Chơi thôi", True, BLACK)
    submit_label_x = submit_button.x + (submit_button.width - submit_label.get_width()) // 2
    submit_label_y = submit_button.y + (submit_button.height - submit_label.get_height()) // 2

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_RETURN:
                    # Process login here
                    print("mssv:", username_value) # Sửa
                    print("email:", email_value)
                    print("name:", password_value)
                elif username.collidepoint(pygame.mouse.get_pos()) and event.key == K_BACKSPACE:
                    username_value = username_value[:-1]
                elif email.collidepoint(pygame.mouse.get_pos()) and event.key == K_BACKSPACE:
                    email_value = email_value[:-1]
                elif password.collidepoint(pygame.mouse.get_pos()) and event.key == K_BACKSPACE:
                    password_value = password_value[:-1]
                else:
                    if username.collidepoint(pygame.mouse.get_pos()):
                        username_value += event.unicode
                    elif email.collidepoint(pygame.mouse.get_pos()):
                        email_value += event.unicode
                    elif password.collidepoint(pygame.mouse.get_pos()):
                        password_value += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                if submit_button.collidepoint(pygame.mouse.get_pos()):
                    data = {
                        'mssv': username_value,
                        'email': email_value,
                        'name': password_value
                    }
                    return data
                    
        # Clear the window
        window.fill(WHITE)

        # Render the sentence
        sentence = font.render("NHẬP THÔNG TIN NGƯỜI CHƠI", True, BLACK)
        window.blit(sentence, (50, 50))

        # Draw the text inputs
        pygame.draw.rect(window, BLACK, username, 2)
        pygame.draw.rect(window, BLACK, email, 2)
        pygame.draw.rect(window, BLACK, password, 2)

        # Render the labels
        username_label = font.render("MSSV:", True, BLACK)
        email_label = font.render("Email:", True, BLACK)
        password_label = font.render("Tên cuối:", True, BLACK)
        window.blit(username_label, (50, 100))
        window.blit(email_label, (50, 150))
        window.blit(password_label, (50, 200))

        # Render the input values
        username_text = font.render(username_value, True, BLACK)
        email_text = font.render(email_value, True, BLACK)
        password_text = font.render(password_value, True, BLACK)

        if email_text.get_width() > email.width - 10:
            email_width = email_text.get_width() + 10
            email.width = email_width

        if email_text.get_width() > email.width - 10:
            email_text_x = email.x + 5 - (email_text.get_width() - email.width + 10)
        else:
            email_text_x = email.x + 5

        window.blit(username_text, (username.x + 5, username.y + 5))
        window.blit(email_text, (email_text_x, email.y + 5))
        window.blit(password_text, (password.x + 5, password.y + 5))
        # Draw the submit button with rounded corners
        pygame.draw.rect(window, LIGHT_BLUE, submit_button, border_radius=10)
        window.blit(submit_label, (submit_label_x, submit_label_y))
        # Update the display
        pygame.display.update()