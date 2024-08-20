USE `mcu-course`;

CREATE TABLE `teachers` (
    `teacher_id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
);

CREATE TABLE `courses` (
    `course_id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `course_name` VARCHAR(100) NOT NULL,
    `teacher_id` BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (`teacher_id`) REFERENCES `teachers`(`teacher_id`) ON DELETE CASCADE
);

CREATE TABLE `students` (
    `student_id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `option_student_id` VARCHAR(50)
);

CREATE TABLE `student_courses` (
    `student_id` BIGINT UNSIGNED NOT NULL,
    `course_id` BIGINT UNSIGNED NOT NULL,
    `enrollment_date` DATE NOT NULL,
    PRIMARY KEY (`student_id`, `course_id`),
    FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`) ON DELETE CASCADE,
    FOREIGN KEY (`course_id`) REFERENCES `courses`(`course_id`) ON DELETE CASCADE
);
