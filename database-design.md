I'll design a comprehensive database model for your appointment scheduling application, following best practices for relational database design.
Core Tables
1. Businesses
businesses
- id: uuid PRIMARY KEY
- name: text NOT NULL
- address: text
- city: text
- state: text
- postal_code: text
- email: text
- phone: text
- website: text
- created_at: timestamp with time zone DEFAULT now()
- updated_at: timestamp with time zone DEFAULT now()
2. Business Hours
business_hours
- id: uuid PRIMARY KEY
- business_id: uuid REFERENCES businesses(id)
- day_of_week: integer NOT NULL (0-6, where 0 is Sunday)
- open_time: time NOT NULL
- close_time: time NOT NULL
- is_closed: boolean DEFAULT false
3. Services
services
- id: uuid PRIMARY KEY
- business_id: uuid REFERENCES businesses(id)
- name: text NOT NULL
- description: text
- duration: interval NOT NULL
- price: decimal(10,2)
- active: boolean DEFAULT true
- created_at: timestamp with time zone DEFAULT now()
- updated_at: timestamp with time zone DEFAULT now()
4. Clients
clients
- id: uuid PRIMARY KEY
- first_name: text NOT NULL
- last_name: text NOT NULL
- email: text
- phone: text
- notes: text
- created_at: timestamp with time zone DEFAULT now()
- updated_at: timestamp with time zone DEFAULT now()
5. Appointments
appointments
- id: uuid PRIMARY KEY
- business_id: uuid REFERENCES businesses(id)
- service_id: uuid REFERENCES services(id)
- client_id: uuid REFERENCES clients(id)
- staff_id: uuid REFERENCES staff(id) (optional, if you have staff)
- start_time: timestamp with time zone NOT NULL
- end_time: timestamp with time zone NOT NULL
- status: text NOT NULL (e.g., 'scheduled', 'completed', 'cancelled', 'no-show')
- notes: text
- created_at: timestamp with time zone DEFAULT now()
- updated_at: timestamp with time zone DEFAULT now()
Additional Recommended Tables
6. Staff (if applicable)
staff
- id: uuid PRIMARY KEY
- business_id: uuid REFERENCES businesses(id)
- first_name: text NOT NULL
- last_name: text NOT NULL
- email: text
- phone: text
- role: text
- active: boolean DEFAULT true
- created_at: timestamp with time zone DEFAULT now()
- updated_at: timestamp with time zone DEFAULT now()
7. Staff Services (for many-to-many relationship)
staff_services
- id: uuid PRIMARY KEY
- staff_id: uuid REFERENCES staff(id)
- service_id: uuid REFERENCES services(id)
8. Staff Availability
staff_availability
- id: uuid PRIMARY KEY
- staff_id: uuid REFERENCES staff(id)
- day_of_week: integer NOT NULL (0-6, where 0 is Sunday)
- start_time: time NOT NULL
- end_time: time NOT NULL
- is_available: boolean DEFAULT true
Design Decisions and Normalization

Separate Business Hours Table: I've normalized business hours into a separate table to allow for different hours on different days and special cases like holidays.
Appointment Start and End Times: Instead of storing duration with the appointment, I'm storing explicit end_time for clarity and to make querying for available time slots easier.
Staff and Services Relationship: I've created a many-to-many relationship between staff and services, as typically different staff members can provide different subsets of services.
Status as Text Field: For appointment status, I've used a text field, but you might consider using an enum type in PostgreSQL for better data integrity.
UUIDs as Primary Keys: I've chosen UUIDs rather than serial integers for better security and to facilitate distributed systems if needed in the future.

Recommended Indexes
sql-- For appointments
CREATE INDEX idx_appointments_business_id ON appointments(business_id);
CREATE INDEX idx_appointments_client_id ON appointments(client_id);
CREATE INDEX idx_appointments_service_id ON appointments(service_id);
CREATE INDEX idx_appointments_staff_id ON appointments(staff_id);
CREATE INDEX idx_appointments_start_time ON appointments(start_time);
CREATE INDEX idx_appointments_status ON appointments(status);

-- For service lookups
CREATE INDEX idx_services_business_id ON services(business_id);
CREATE INDEX idx_services_active ON services(active);

-- For staff lookups
CREATE INDEX idx_staff_business_id ON staff(business_id);
CREATE INDEX idx_staff_active ON staff(active);
Additional Considerations

Soft Delete: Consider adding a deleted_at timestamp column to tables where you might want to support soft deletes.
Time Zones: Use timestamp with time zone to properly handle appointments across different time zones.
Client Authentication: If clients will log in to make appointments, consider adding authentication fields to the clients table or creating a separate users table.
Recurring Appointments: If you need to support recurring appointments, consider adding a recurring_rule field to appointments or creating a separate recurring_appointments table.