-- Left of when OOP starts 1h 33m

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243

PADDLE_SPEED = 200
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 30

push = require 'push'
Class = require 'class'
require 'Paddle'
require 'Ball'

function love.load()
    love.graphics.setDefaultFilter('nearest', 'nearest')
    love.window.setTitle('My_Pong')
    math.randomseed(os.time())
    
    smallFont =  love.graphics.newFont('assets/ByteBounce.ttf', 8)
    largeFont =  love.graphics.newFont('assets/ByteBounce.ttf', 32)
    scoreFont =  love.graphics.newFont('assets/ByteBounce.ttf', 16)
    
    sounds = {['hit1'] = love.audio.newSource('assets/hit1.wav'),
    ['hit1'] = love.audio.newSource('assets/hit2.wav'),
    ['win'] = love.audio.newSource('assets/win.wav'),
    ['point'] = love.audio.newSource('assets/point.wav'),
    }
    music = love.audio.newSource('assets/music.wav')

    p1_score = 0
    p2_score = 0
    
    p1_y = 10
    p2_y = VIRTUAL_HEIGHT - 40
    

    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
        resizable = false,
        vsync = true,
        fullscreen = false})
        

        -- ball
        ball_size = 10
        ballX = VIRTUAL_WIDTH / 2 - ball_size
        ballY = VIRTUAL_HEIGHT / 2 - ball_size

        ballDX = math.random(2) == 1 and 100 or - 100
        ballDY = math.random(-50, 50)
        
        gameState = 'start'
    end
    
    function love.keypressed(key)
        if key == 'escape' then
            love.event.quit()
        elseif key == 'return' then
            if gameState == 'start' then
                gameState = 'play'
            else
                gameState = 'start'
                
                ballX = VIRTUAL_WIDTH / 2 - ball_size
                ballY = VIRTUAL_HEIGHT / 2 - ball_size
                
                ballDX = math.random(2) == 1 and 100 or - 100
                ballDY = math.random(-50, 50)
            end
    end
end

function love.update(dt)
    if love.keyboard.isDown('w') then
        p1_y = p1_y + -PADDLE_SPEED * dt
    elseif love.keyboard.isDown('s') then
        p1_y = p1_y + PADDLE_SPEED * dt
    end

    if love.keyboard.isDown('up') then
        p2_y = p2_y + -PADDLE_SPEED * dt
    elseif love.keyboard.isDown('down') then
        p2_y = p2_y + PADDLE_SPEED * dt
    end

    -- clamp movement
    if p1_y < 0 then
        p1_y = 0
    elseif p1_y > VIRTUAL_HEIGHT - PADDLE_HEIGHT then
        p1_y = VIRTUAL_HEIGHT - PADDLE_HEIGHT
    end
    if p2_y < 0 then
        p2_y = 0
    elseif p2_y > VIRTUAL_HEIGHT - PADDLE_HEIGHT then
        p2_y = VIRTUAL_HEIGHT - PADDLE_HEIGHT
    end

    if gameState == 'play' then
        ballX = ballX + ballDX * dt
        ballY = ballY + ballDY * dt
    end
end

function love.draw()
    push:start()
    love.graphics.clear(40/255,45/255,70/255,1)
    love.graphics.setFont(largeFont)
    love.graphics.print(tostring(p1_score), VIRTUAL_WIDTH/2 - 50, 30)
    love.graphics.print(tostring(p2_score), VIRTUAL_WIDTH/2 + 30, 30)

    -- paddle 1
    love.graphics.rectangle('fill', 10, p1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    -- paddle 2
    love.graphics.rectangle('fill', VIRTUAL_WIDTH -20, p2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    -- ball
    love.graphics.rectangle('fill', ballX, ballY, ball_size, ball_size)

    if gameState == 'start' then
        love.graphics.setFont(smallFont)
        love.graphics.printf('Press ENTER to start', 0, VIRTUAL_HEIGHT * 0.85, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('or restart at any time', 0, VIRTUAL_HEIGHT * 0.9, VIRTUAL_WIDTH, 'center')
    end

    push:finish()
end