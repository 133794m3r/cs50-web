Paddle = Class{}

function Paddle:init(x,y,width,height)
	self.x=x
	self.y=y
	self.width=width
	self.height=height
	self.dy=0
end

function Paddle:update(dt)

	if self.dy < 0 then
		self.y = math.max(0,self.y+self.dy*dt)
	else
		self.y = math.min(VIRTUAL_HEIGHT - self.height, self.y+self.dy*dt)
	end
end

function Paddle:draw()
    love.graphics.rectangle('fill', self.x, self.y, self.width, self.height)
end

Ai = Class{}


function Ai:init(level, move_speed)
	self.level = level
	self.move_speed = move_speed
	self.cur_bonus = 0
end


function Ai:update()
	local move_check = math.random(10);
	if move_check <= (self.level+self.cur_bonus) then
		if ball.y > player2.y then
			player2.dy = self.move_speed
			player2:update(1)
	else
		self.cur_bonus = self.cur_bonus + 1
	end
end
