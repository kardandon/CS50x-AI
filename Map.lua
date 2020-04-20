--[[
    Contains tile data and necessary code for rendering a tile map to the
    screen.
]]

require 'Util'

Map = Class{}

TILE_BRICK = 1
TILE_EMPTY = -1

-- cloud tiles
CLOUD_LEFT = 6
CLOUD_RIGHT = 7

-- flag_bar

FLAG_BOTTOM = 16
FLAG_MIDDLE = 12
FLAG_TOP = 8

-- bush tiles
BUSH_LEFT = 2
BUSH_RIGHT = 3

-- mushroom tiles
MUSHROOM_TOP = 10
MUSHROOM_BOTTOM = 11

-- jump block
JUMP_BLOCK = 5
JUMP_BLOCK_HIT = 9

DEATH_STATE = 0
-- a speed to multiply delta time to scroll map; smooth value
local SCROLL_SPEED = 62

-- constructor for our map object
function Map:init()

    self.spritesheet = love.graphics.newImage('graphics/spritesheet.png')
    self.sprites = generateQuads(self.spritesheet, 16, 16)
    --self.music = love.audio.newSource('sounds/music.wav', 'static')
    self.currentflag = nil
    self.flaganimation =
    Animation({
        frames = {
            texture = self.spritesheet,
            love.graphics.newQuad(0, 16 * 3, 16, 16, self.spritesheet:getDimensions()),
            love.graphics.newQuad(16 * 1, 16 * 3, 16, 16, self.spritesheet:getDimensions()),
            love.graphics.newQuad(16 * 2, 16 * 3, 16, 16, self.spritesheet:getDimensions()),
        },
        interval = 0.15
    })
    self.endgame = 16
    self.tileWidth = 16
    self.tileHeight = 16
    self.mapWidth = math.random(100,200)
    self.mapHeight = 28
    self.tiles = {}
    self.flaglocation = 4

    -- applies positive Y influence on anything affected
    self.gravity = 15

    -- associate player with map
    self.player = Player(self)

    -- camera offsets
    self.camX = 0
    self.camY = -3

    -- cache width and height of map in pixels
    self.mapWidthPixels = self.mapWidth * self.tileWidth
    self.mapHeightPixels = self.mapHeight * self.tileHeight
    self.player.maxwidth = self.mapWidthPixels

    self.currentflag = self.flaganimation:getCurrentFrame()

    for y = 1, self.mapHeight do
        for x = 1, self.mapWidth do
            
            -- support for multiple sheets per tile; storing tiles as tables 
            self:setTile(x, y, TILE_EMPTY)
        end
    end

    -- first, fill map with empty tiles


    -- begin generating the terrain using vertical scan lines
    
    --     
    --     self:setTile(x,self.mapHeight -1, TILE_BRICK)
    --     for y =  self.mapHeight-2, self.mapHeight -5 + x - self.mapWidth + 9, -1 do
    --         self:setTile(x,y, TILE_BRICK)
    --     end
    -- end

    -- start the background music
    --self.music:setLooping(true)
    --self.music:play()
end

function Map:generateWorld()
    for y = 1, self.mapHeight do
        for x = 1, self.mapWidth do
            
            -- support for multiple sheets per tile; storing tiles as tables 
            self:setTile(x, y, TILE_EMPTY)
        end
    end
    local x = 1
    while x <= self.mapWidth do
        if x == self.tileWidth * 10 then
            for y = self.mapHeight / 2, self.mapHeight do
                self:setTile(x, y, TILE_BRICK)
            end
        -- 2% chance to generate a cloud
        -- make sure we're 2 tiles from edge at least
        elseif x < self.mapWidth - self.endgame then
            if x < self.mapWidth - 2 then
                if math.random(7) == 1 then
                    
                    -- choose a random vertical spot above where blocks/pipes generate
                    local cloudStart = math.random(self.mapHeight / 2 - 6)

                    self:setTile(x, cloudStart, CLOUD_LEFT)
                    self:setTile(x + 1, cloudStart, CLOUD_RIGHT)
                end
            end

            -- 5% chance to generate a mushroom
            if math.random(20) == 1 then
                -- left side of pipe
                self:setTile(x, self.mapHeight / 2 - 2, MUSHROOM_TOP)
                self:setTile(x, self.mapHeight / 2 - 1, MUSHROOM_BOTTOM)

                -- creates column of tiles going to bottom of map
                for y = self.mapHeight / 2, self.mapHeight do
                    self:setTile(x, y, TILE_BRICK)
                end

                -- next vertical scan line
                x = x + 1

            -- 10% chance to generate bush, being sure to generate away from edge
            elseif math.random(10) == 1 and x < self.mapWidth - 3 then
                local bushLevel = self.mapHeight / 2 - 1

                -- place bush component and then column of bricks
                self:setTile(x, bushLevel, BUSH_LEFT)
                for y = self.mapHeight / 2, self.mapHeight do
                    self:setTile(x, y, TILE_BRICK)
                end
                x = x + 1

                self:setTile(x, bushLevel, BUSH_RIGHT)
                for y = self.mapHeight / 2, self.mapHeight do
                    self:setTile(x, y, TILE_BRICK)
                end
                x = x + 1

            -- 10% chance to not generate anything, creating a gap
            elseif math.random(10) ~= 1 then
                
                -- creates column of tiles going to bottom of map
                for y = self.mapHeight / 2, self.mapHeight do
                    self:setTile(x, y, TILE_BRICK)
                end

                -- chance to create a block for Mario to hit
                if math.random(15) == 1 then
                    self:setTile(x, self.mapHeight / 2 - 4, JUMP_BLOCK)
                end

                -- next vertical scan line
                x = x + 1
            elseif x ~= map.tileWidth * 10 - 1 then
                -- increment X so we skip two scanlines, creating a 2-tile gap
                x = x + 2
            end
        else
            local i = 1
            while x < self.mapWidth - self.endgame + 7 do
                if i == 7 then
                    for y = self.mapHeight / 2 - 6, self.mapHeight do
                        self:setTile(x, y, TILE_BRICK)
                    end
                else
                    for y = self.mapHeight / 2 - i, self.mapHeight do
                        self:setTile(x, y, TILE_BRICK)
                    end
                end
                i = i + 1
                x = x + 1
            end
            for y = self.mapHeight / 2, self.mapHeight do
                self:setTile(x, y, TILE_BRICK)
            end
            if (x == self.mapWidth - self.flaglocation) then
                self:setTile(x, self.mapHeight / 2 - 7, FLAG_TOP)
                self:setTile(x, self.mapHeight / 2 - 1, FLAG_BOTTOM)
                for y = self.mapHeight / 2 - 6 , self.mapHeight / 2 - 1 do
                    self:setTile(x, y, FLAG_MIDDLE)
                end
            end
            x = x + 1
        end
    end
end

-- return whether a given tile is collidable
function Map:collides(tile)
    -- define our collidable tiles
    local collidables = {
        TILE_BRICK, JUMP_BLOCK, JUMP_BLOCK_HIT,
        MUSHROOM_TOP, MUSHROOM_BOTTOM
    }

    -- iterate and return true if our tile type matches
    for _, v in ipairs(collidables) do
        if tile.id == v then
            return true
        end
    end

    return false
end

-- function to update camera offset with delta time
function Map:update(dt)
    if self.player.state ~= 'win' then
        self.flaganimation:update(dt)
        self.currentflag = self.flaganimation:getCurrentFrame()
    end
    if self.player.x >= self.mapWidthPixels - 5 * self.tileWidth then
        self.currentflag = love.graphics.newQuad(16 * 2, 16 * 3, 16, 16, self.spritesheet:getDimensions())
        self.player:win()
    end
    if  self.player.y >= VIRTUAL_HEIGHT  and DEATH_STATE == 0 then
        self.player.y = VIRTUAL_HEIGHT - 1
        self.player:death()
        DEATH_STATE = 1
    elseif DEATH_STATE == 1 and self.player.y >= VIRTUAL_HEIGHT then
        self.player:reset()
        DEATH_STATE = 0
    end

    self.player:update(dt)

    -- keep camera's X coordinate following the player, preventing camera from
    -- scrolling past 0 to the left and the map's width
    self.camX = --self.player.x- VIRTUAL_WIDTH / 2
        math.max(0, math.min(self.player.x- VIRTUAL_WIDTH / 2,
        math.min(self.mapWidthPixels - VIRTUAL_WIDTH, self.player.x)))
end

-- gets the tile type at a given pixel coordinate
function Map:tileAt(x, y)
    return {
        x = math.floor(x / self.tileWidth) + 1,
        y = math.floor(y / self.tileHeight) + 1,
        id = self:getTile(math.floor(x / self.tileWidth) + 1, math.floor(y / self.tileHeight) + 1)
    }
end


-- returns an integer value for the tile at a given x-y coordinate
function Map:getTile(x, y)
    return self.tiles[(y - 1) * self.mapWidth + x]
end

-- sets a tile at a given x-y coordinate to an integer value
function Map:setTile(x, y, id)
    self.tiles[(y - 1) * self.mapWidth + x] = id
end

-- renders our map to the screen, to be called by main's render
function Map:render()
    for y = 1, self.mapHeight do
        for x = 1, self.mapWidth do
            local tile = self:getTile(x, y)
            if tile ~= TILE_EMPTY then
                love.graphics.draw(self.spritesheet, self.sprites[tile],
                    (x - 1) * self.tileWidth, (y - 1) * self.tileHeight)
                if x == self.mapWidth - 4 and y == self.mapHeight / 2 - 7 then
                    love.graphics.draw(self.spritesheet, self.currentflag,
                    (x) * self.tileWidth, (y - 1) * self.tileHeight)
                end
            end
        end
    end

    self.player:render()
end
