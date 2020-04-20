--[[
    Super Mario Bros. Demo
    Author: Colton Ogden
    Original Credit: Nintendo

    Demonstrates rendering a screen of tiles.
]]

Class = require 'class'
push = require 'push'

require 'Animation'
require 'Map'
require 'Player'

-- close resolution to NES but 16:9
VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243

-- actual window resolution
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FULLSCREEN = false

-- seed RNG
math.randomseed(os.time())

-- makes upscaling look pixel-y instead of blurry
love.graphics.setDefaultFilter('nearest', 'nearest')

-- an object to contain our map data
map = Map()

-- performs initialization of all objects and data needed by program
function love.load()
    largeFont = love.graphics.newFont('font.ttf', 32)
    smallFont = love.graphics.newFont('font.ttf', 16)
    selectMenu = 0
    win_sound = love.audio.newSource('sounds/pickup.wav', 'static')
    -- sets up a different, better-looking retro font as our default
    love.graphics.setFont(love.graphics.newFont('fonts/font.ttf', 8))

    gameState = 'mainmenu'

    -- sets up virtual screen resolution for an authentic retro feel
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
        fullscreen = FULLSCREEN,
        vsync = true,
        resizable = true
    })

    love.window.setTitle('Space Mario')

    love.keyboard.keysPressed = {}
    love.keyboard.keysReleased = {}
end

-- called whenever window is resized
function love.resize(w, h)
    push:resize(w, h)
end

-- global key pressed function
function love.keyboard.wasPressed(key)
    if (love.keyboard.keysPressed[key]) then
        return true
    else
        return false
    end
end

-- global key released function
function love.keyboard.wasReleased(key)
    if (love.keyboard.keysReleased[key]) then
        return true
    else
        return false
    end
end

-- called whenever a key is pressed
function love.keypressed(key)
    if key == 'escape' then
        gameState = 'mainmenu'
    end
    if gameState == 'mainmenu' then
        if love.keyboard.isDown('down') then
            selectMenu = selectMenu >= 3 and 0 or selectMenu + 1
        elseif love.keyboard.isDown('up') then
            selectMenu = selectMenu == 0 and 3 or selectMenu - 1
        elseif love.keyboard.isDown('kpenter') or love.keyboard.isDown('return') then
            if selectMenu == 0 then
                map:generateWorld()
                map.player:reset()
                gameState = 'play'
            elseif selectMenu == 1 then
                gameState = 'howtoplay'
            elseif selectMenu == 2 then
                gameState = 'options'
            else
                love.event.quit()
            end
        end
    elseif gameState == 'win' then
        if love.keyboard.isDown('kpenter') or love.keyboard.isDown('return') then
            gameState = 'mainmenu'
        elseif key == 'escape' then
            love.event.quit()
        end
    elseif gameState == 'howtoplay' then
        if love.keyboard.isDown('kpenter') or love.keyboard.isDown('return') then
            gameState = 'mainmenu'
        end
    elseif gameState == 'options' then
        if love.keyboard.isDown('kpenter') or love.keyboard.isDown('return') then
            if selectMenu == 0 then
                FULLSCREEN = not FULLSCREEN
                love.load()
            else
                gameState = 'mainmenu'
            end
        elseif love.keyboard.isDown('up') then
            selectMenu = selectMenu >= 1 and 0 or 1
        elseif love.keyboard.isDown('down') then
            selectMenu = selectMenu <=0 and 1 or 0
        end
    elseif gameState == 'play' then
        love.keyboard.keysPressed[key] = true
    end
end

-- called whenever a key is released
function love.keyreleased(key)

    love.keyboard.keysReleased[key] = true

end

-- called every frame, with dt passed in as delta in time since last frame
function love.update(dt)
    if gameState == 'play' then
        map:update(dt)
    end
    if map.player.winbool == true then
        win_sound:play()
        gameState = 'win'
        map.player.winbool = false
    end
    -- reset all keys pressed and released this frame
    love.keyboard.keysPressed = {}
    love.keyboard.keysReleased = {}
end

-- called each frame, used to render to the screen
function love.draw()
    -- begin virtual resolution drawing
    push:apply('start')

    -- clear screen using Mario background blue
    love.graphics.clear(108/255, 140/255, 255/255, 255/255)
    
    -- renders our map object onto the screen
    if gameState == 'play' then
        love.graphics.translate(math.floor(-map.camX + 0.5), math.floor(-map.camY + 0.5))
        map:render()
    elseif gameState == 'win' then
        love.graphics.setFont(largeFont)
        love.graphics.printf('Thank You for playing\nSPACE MARIO', 0, 30, VIRTUAL_WIDTH, 'center')
        love.graphics.setFont(smallFont)
        love.graphics.printf('Press enter to back to mainmenu', 0, 110, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('Press ESC to exit', 0, 130, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'mainmenu' then
        love.graphics.setFont(largeFont)
        love.graphics.printf('SPACE MARIO', 0, 30, VIRTUAL_WIDTH, 'center')
        love.graphics.setFont(smallFont)
        if selectMenu == 0 then
            love.graphics.printf('> PLAY SPACE MARIO', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('How To Play', 0, 130, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Options', 0, 150, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Exit', 0, 200, VIRTUAL_WIDTH, 'center')
        elseif selectMenu == 1 then
            love.graphics.printf('PLAY SPACE MARIO', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('> How To Play', 0, 130, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Options', 0, 150, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Exit', 0, 200, VIRTUAL_WIDTH, 'center')
        elseif selectMenu == 2 then
            love.graphics.printf('PLAY SPACE MARIO', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('How To Play', 0, 130, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('> Options', 0, 150, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Exit', 0, 200, VIRTUAL_WIDTH, 'center')
        else
            love.graphics.printf('PLAY SPACE MARIO', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('How To Play', 0, 130, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Options', 0, 150, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('> Exit', 0, 200, VIRTUAL_WIDTH, 'center')
        end
    elseif gameState == 'howtoplay' then
        love.graphics.setFont(largeFont)
        love.graphics.printf('SPACE MARIO', 0, 30, VIRTUAL_WIDTH, 'center')
        love.graphics.setFont(smallFont)
        love.graphics.printf('Press space or up to jump\n Press left to go left \n Press right to go right \n Press ESC to escape to mainmenu', 0, 110, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('> Return to main menu', 0, 200, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'options' then
        love.graphics.setFont(largeFont)
        love.graphics.printf('SPACE MARIO', 0, 30, VIRTUAL_WIDTH, 'center')
        love.graphics.setFont(smallFont)
        if selectMenu == 0 then
            love.graphics.printf('> Fullscreen', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('Return to main menu', 0, 200, VIRTUAL_WIDTH, 'center')
        else
            love.graphics.printf('Fullscreen', 0, 110, VIRTUAL_WIDTH, 'center')
            love.graphics.printf('> Return to main menu', 0, 200, VIRTUAL_WIDTH, 'center')
        end

        
    end

    -- end virtual resolution
    push:apply('end')
end
