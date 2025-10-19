import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SyllabusExtractor:
    """
    AI-powered syllabus extraction service
    Extracts structured data from syllabus text using pattern matching and NLP techniques
    """
    
    def __init__(self):
        self.date_patterns = [
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b',
            r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b'
        ]
        
        self.time_patterns = [
            r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b',
            r'\b\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b',
            r'\b\d{1,2}:\d{2}\s*to\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b'
        ]
        
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        
    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from syllabus text
        """
        try:
            extraction_data = {
                'course_title': self._extract_course_title(text),
                'course_code': self._extract_course_code(text),
                'course_description': self._extract_course_description(text),
                'credits': self._extract_credits(text),
                'prerequisites': self._extract_prerequisites(text),
                
                'professor_name': self._extract_professor_name(text),
                'professor_email': self._extract_professor_email(text),
                'professor_office': self._extract_professor_office(text),
                'professor_office_hours': self._extract_office_hours(text),
                'professor_phone': self._extract_professor_phone(text),
                
                'class_days': self._extract_class_days(text),
                'class_time': self._extract_class_time(text),
                'class_location': self._extract_class_location(text),
                'semester': self._extract_semester(text),
                
                'exam_dates': self._extract_exam_dates(text),
                'homework_dates': self._extract_homework_dates(text),
                'project_dates': self._extract_project_dates(text),
                'quiz_dates': self._extract_quiz_dates(text),
                'final_exam_date': self._extract_final_exam_date(text),
                'midterm_dates': self._extract_midterm_dates(text),
                
                'grading_scale': self._extract_grading_scale(text),
                'grade_breakdown': self._extract_grade_breakdown(text),
                'late_policy': self._extract_late_policy(text),
                'attendance_policy': self._extract_attendance_policy(text),
                
                'academic_integrity': self._extract_academic_integrity(text),
                'disability_accommodations': self._extract_disability_accommodations(text),
                'course_objectives': self._extract_course_objectives(text),
                
                'textbook_required': self._extract_required_textbooks(text),
                'textbook_recommended': self._extract_recommended_textbooks(text),
                'course_website': self._extract_course_website(text),
                'additional_resources': self._extract_additional_resources(text),
                
                'extraction_confidence': self._calculate_confidence(text),
                'extraction_method': 'ai_extraction'
            }
            
            return extraction_data
            
        except Exception as e:
            logger.error(f"Syllabus extraction failed: {str(e)}")
            return {'extraction_error': str(e), 'extraction_confidence': 0.0}
    
    def _extract_course_title(self, text: str) -> str:
        """Extract course title"""
        patterns = [
            r'Course Title:\s*([^\n]+)',
            r'Title:\s*([^\n]+)',
            r'^([A-Z][^:\n]{10,100})$',  # Lines that look like titles
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_course_code(self, text: str) -> str:
        """Extract course code (e.g., CS101, MATH 201)"""
        patterns = [
            r'Course Code:\s*([A-Z]{2,4}\s*\d{3,4})',
            r'Course Number:\s*([A-Z]{2,4}\s*\d{3,4})',
            r'\b([A-Z]{2,4}\s*\d{3,4})\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_course_description(self, text: str) -> str:
        """Extract course description"""
        patterns = [
            r'Course Description:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Description:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Overview:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_credits(self, text: str) -> Optional[int]:
        """Extract credit hours"""
        patterns = [
            r'Credits?:\s*(\d+)',
            r'Credit Hours?:\s*(\d+)',
            r'(\d+)\s*credits?',
            r'(\d+)\s*credit hours?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_prerequisites(self, text: str) -> str:
        """Extract prerequisites"""
        patterns = [
            r'Prerequisites?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Prereq:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_professor_name(self, text: str) -> str:
        """Extract professor name"""
        patterns = [
            r'Instructor:\s*([^\n]+)',
            r'Professor:\s*([^\n]+)',
            r'Faculty:\s*([^\n]+)',
            r'Dr\.\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'Professor\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_professor_email(self, text: str) -> str:
        """Extract professor email"""
        emails = re.findall(self.email_pattern, text)
        # Look for emails near instructor/professor sections
        instructor_section = re.search(r'(?:Instructor|Professor|Faculty):[^@]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', text, re.IGNORECASE)
        if instructor_section:
            return instructor_section.group(1)
        return emails[0] if emails else ""
    
    def _extract_professor_office(self, text: str) -> str:
        """Extract professor office location"""
        patterns = [
            r'Office:\s*([^\n]+)',
            r'Office Location:\s*([^\n]+)',
            r'Room:\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_office_hours(self, text: str) -> str:
        """Extract office hours"""
        patterns = [
            r'Office Hours?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Hours?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_professor_phone(self, text: str) -> str:
        """Extract professor phone number"""
        phones = re.findall(self.phone_pattern, text)
        return phones[0] if phones else ""
    
    def _extract_class_days(self, text: str) -> str:
        """Extract class meeting days"""
        patterns = [
            r'Days?:\s*([^\n]+)',
            r'Meeting Days?:\s*([^\n]+)',
            r'(?:MWF|TTh|MTWThF|MW|TThF)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_class_time(self, text: str) -> str:
        """Extract class meeting time"""
        times = re.findall(r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)', text)
        return times[0] if times else ""
    
    def _extract_class_location(self, text: str) -> str:
        """Extract class location"""
        patterns = [
            r'Location:\s*([^\n]+)',
            r'Room:\s*([^\n]+)',
            r'Building:\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_semester(self, text: str) -> str:
        """Extract semester information"""
        patterns = [
            r'Semester:\s*([^\n]+)',
            r'Term:\s*([^\n]+)',
            r'(?:Fall|Spring|Summer|Winter)\s+\d{4}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_exam_dates(self, text: str) -> List[Dict]:
        """Extract exam dates"""
        exam_keywords = ['exam', 'test', 'midterm', 'final']
        dates = []
        
        for keyword in exam_keywords:
            pattern = rf'\b{keyword}[^:\n]*:\s*([^\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match)
                if date_match:
                    dates.append({
                        'title': f"{keyword.title()}",
                        'date': date_match.group(1),
                        'type': 'exam'
                    })
        
        return dates
    
    def _extract_homework_dates(self, text: str) -> List[Dict]:
        """Extract homework due dates"""
        homework_keywords = ['homework', 'assignment', 'hw', 'due']
        dates = []
        
        for keyword in homework_keywords:
            pattern = rf'\b{keyword}[^:\n]*:\s*([^\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match)
                if date_match:
                    dates.append({
                        'title': f"{keyword.title()}",
                        'date': date_match.group(1),
                        'type': 'homework'
                    })
        
        return dates
    
    def _extract_project_dates(self, text: str) -> List[Dict]:
        """Extract project due dates"""
        project_keywords = ['project', 'presentation', 'report']
        dates = []
        
        for keyword in project_keywords:
            pattern = rf'\b{keyword}[^:\n]*:\s*([^\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match)
                if date_match:
                    dates.append({
                        'title': f"{keyword.title()}",
                        'date': date_match.group(1),
                        'type': 'project'
                    })
        
        return dates
    
    def _extract_quiz_dates(self, text: str) -> List[Dict]:
        """Extract quiz dates"""
        quiz_keywords = ['quiz', 'quizzes']
        dates = []
        
        for keyword in quiz_keywords:
            pattern = rf'\b{keyword}[^:\n]*:\s*([^\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match)
                if date_match:
                    dates.append({
                        'title': f"{keyword.title()}",
                        'date': date_match.group(1),
                        'type': 'quiz'
                    })
        
        return dates
    
    def _extract_final_exam_date(self, text: str) -> Optional[datetime]:
        """Extract final exam date"""
        pattern = r'final\s+exam[^:\n]*:\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match.group(1))
            if date_match:
                try:
                    return datetime.strptime(date_match.group(1), '%m/%d/%Y')
                except ValueError:
                    try:
                        return datetime.strptime(date_match.group(1), '%Y-%m-%d')
                    except ValueError:
                        pass
        return None
    
    def _extract_midterm_dates(self, text: str) -> List[Dict]:
        """Extract midterm dates"""
        midterm_keywords = ['midterm', 'mid-term']
        dates = []
        
        for keyword in midterm_keywords:
            pattern = rf'\b{keyword}[^:\n]*:\s*([^\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})', match)
                if date_match:
                    dates.append({
                        'title': f"{keyword.title()}",
                        'date': date_match.group(1),
                        'type': 'midterm'
                    })
        
        return dates
    
    def _extract_grading_scale(self, text: str) -> str:
        """Extract grading scale"""
        patterns = [
            r'Grading Scale:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Grade Scale:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_grade_breakdown(self, text: str) -> Dict[str, int]:
        """Extract grade breakdown percentages"""
        breakdown = {}
        patterns = [
            r'(\w+)\s*:\s*(\d+)%',
            r'(\w+)\s*=\s*(\d+)%',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                breakdown[match[0].lower()] = int(match[1])
        
        return breakdown
    
    def _extract_late_policy(self, text: str) -> str:
        """Extract late submission policy"""
        patterns = [
            r'Late Policy:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Late Work:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_attendance_policy(self, text: str) -> str:
        """Extract attendance policy"""
        patterns = [
            r'Attendance Policy:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Attendance:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_academic_integrity(self, text: str) -> str:
        """Extract academic integrity policy"""
        patterns = [
            r'Academic Integrity:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Honor Code:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_disability_accommodations(self, text: str) -> str:
        """Extract disability accommodations policy"""
        patterns = [
            r'Disability Accommodations?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Accommodations?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_course_objectives(self, text: str) -> str:
        """Extract course objectives"""
        patterns = [
            r'Course Objectives?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Learning Objectives?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Objectives?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_required_textbooks(self, text: str) -> str:
        """Extract required textbooks"""
        patterns = [
            r'Required Textbooks?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Textbooks?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_recommended_textbooks(self, text: str) -> str:
        """Extract recommended textbooks"""
        patterns = [
            r'Recommended Textbooks?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Optional Textbooks?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_course_website(self, text: str) -> str:
        """Extract course website URL"""
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        return urls[0] if urls else ""
    
    def _extract_additional_resources(self, text: str) -> str:
        """Extract additional resources"""
        patterns = [
            r'Additional Resources?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'Resources?:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate extraction confidence based on found patterns"""
        confidence = 0.0
        total_patterns = 20  # Number of extraction methods
        
        # Check for key syllabus elements
        key_elements = [
            'course', 'instructor', 'professor', 'syllabus', 'schedule',
            'grading', 'exam', 'homework', 'assignment', 'textbook'
        ]
        
        found_elements = sum(1 for element in key_elements if element.lower() in text.lower())
        confidence += (found_elements / len(key_elements)) * 0.5
        
        # Check for structured formatting
        if re.search(r'Course\s*:', text, re.IGNORECASE):
            confidence += 0.1
        if re.search(r'Instructor\s*:', text, re.IGNORECASE):
            confidence += 0.1
        if re.search(r'Grading\s*:', text, re.IGNORECASE):
            confidence += 0.1
        if re.search(r'Schedule\s*:', text, re.IGNORECASE):
            confidence += 0.1
        
        # Check for dates
        if re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', text):
            confidence += 0.1
        
        return min(confidence, 1.0)
