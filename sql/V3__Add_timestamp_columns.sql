ALTER TABLE availabilities
ADD created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
ADD updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;