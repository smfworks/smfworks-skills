#!/usr/bin/env python3
"""
Test Suite for SMF Works Skills
Tests all 10 free skills for functionality and correctness.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add skills to path
sys.path.insert(0, str(Path(__file__).parent / "skills"))

class SkillTester:
    def __init__(self):
        self.test_results = []
        self.temp_dir = tempfile.mkdtemp(prefix="smf_test_")
        
    def cleanup(self):
        """Clean up temporary test files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def log(self, skill_name: str, test_name: str, passed: bool, message: str = ""):
        """Log test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            "skill": skill_name,
            "test": test_name,
            "passed": passed,
            "message": message
        })
        print(f"  {status}: {skill_name} - {test_name} {message}")
        return passed
    
    def test_file_organizer(self):
        """Test File Organizer skill."""
        print("\n📁 Testing File Organizer...")
        
        try:
            from file_organizer.main import organize_by_date, organize_by_type, find_duplicates
            
            # Test 1: Organize by date
            test_dir = Path(self.temp_dir) / "test_org_date"
            test_dir.mkdir()
            (test_dir / "test1.txt").write_text("test")
            (test_dir / "test2.txt").write_text("test2")
            
            result = organize_by_date(str(test_dir))
            passed = result.get("success") and result.get("files_moved") == 2
            self.log("File Organizer", "organize_by_date", passed, f"moved {result.get('files_moved', 0)} files")
            
            # Test 2: Find duplicates
            dup_dir = Path(self.temp_dir) / "test_dups"
            dup_dir.mkdir()
            (dup_dir / "file1.txt").write_text("duplicate content")
            (dup_dir / "file2.txt").write_text("duplicate content")
            
            result = find_duplicates(str(dup_dir))
            passed = result.get("success") and result.get("duplicates_found", 0) >= 1
            self.log("File Organizer", "find_duplicates", passed, f"found {result.get('duplicates_found', 0)} dups")
            
        except Exception as e:
            self.log("File Organizer", "import/execution", False, str(e))
    
    def test_pdf_toolkit(self):
        """Test PDF Toolkit skill."""
        print("\n📄 Testing PDF Toolkit...")
        
        try:
            from pdf_toolkit.main import get_pdf_info
            
            # Create a simple test PDF using PyPDF2
            test_pdf = Path(self.temp_dir) / "test.pdf"
            try:
                from PyPDF2 import PdfWriter
                writer = PdfWriter()
                writer.add_blank_page(width=612, height=792)
                with open(test_pdf, 'wb') as f:
                    writer.write(f)
            except:
                # Skip if we can't create PDF
                self.log("PDF Toolkit", "pdf_creation", False, "PyPDF2 not available for testing")
                return
            
            # Test get info
            result = get_pdf_info(str(test_pdf))
            passed = result.get("success") and result.get("pages") == 1
            self.log("PDF Toolkit", "get_pdf_info", passed, f"{result.get('pages', 0)} pages")
            
        except Exception as e:
            self.log("PDF Toolkit", "import/execution", False, str(e))
    
    def test_text_formatter(self):
        """Test Text Formatter skill."""
        print("\n📝 Testing Text Formatter...")
        
        try:
            from text_formatter.main import convert_case, word_count
            
            # Test case conversion
            result = convert_case("hello world", "upper")
            passed = result == "HELLO WORLD"
            self.log("Text Formatter", "convert_case_upper", passed, f"got '{result}'")
            
            # Test title case
            result = convert_case("hello world", "title")
            passed = result == "Hello World"
            self.log("Text Formatter", "convert_case_title", passed, f"got '{result}'")
            
            # Test word count
            result = word_count("hello world test")
            passed = result.get("words") == 3
            self.log("Text Formatter", "word_count", passed, f"{result.get('words')} words")
            
        except Exception as e:
            self.log("Text Formatter", "import/execution", False, str(e))
    
    def test_qr_generator(self):
        """Test QR Generator skill."""
        print("\n📱 Testing QR Generator...")
        
        try:
            from qr_generator.main import generate_qr
            
            # Test basic QR generation
            output_file = Path(self.temp_dir) / "test_qr.png"
            result = generate_qr("https://smf.works", str(output_file))
            passed = result.get("success") and output_file.exists()
            self.log("QR Generator", "generate_qr", passed, f"created {output_file.name if passed else 'failed'}")
            
        except Exception as e:
            self.log("QR Generator", "import/execution", False, str(e))
    
    def test_system_monitor(self):
        """Test System Monitor skill."""
        print("\n💻 Testing System Monitor...")
        
        try:
            from system_monitor.main import get_disk_usage, get_system_info
            
            # Test disk usage
            result = get_disk_usage("/")
            passed = result.get("success") and "total_gb" in result
            self.log("System Monitor", "get_disk_usage", passed, f"{result.get('total_gb', 0)}GB total")
            
            # Test system info
            result = get_system_info()
            passed = result.get("platform") is not None
            self.log("System Monitor", "get_system_info", passed, result.get("platform", "unknown")[:30])
            
        except Exception as e:
            self.log("System Monitor", "import/execution", False, str(e))
    
    def test_website_checker(self):
        """Test Website Checker skill."""
        print("\n🌐 Testing Website Checker...")
        
        try:
            from website_checker.main import check_url
            
            # Test with a reliable site (using httpbin for testing)
            result = check_url("https://httpbin.org/get", timeout=5)
            passed = result.get("success") and result.get("status_code") == 200
            self.log("Website Checker", "check_url", passed, f"status {result.get('status_code')} in {result.get('response_time_ms', 0):.0f}ms")
            
        except Exception as e:
            self.log("Website Checker", "import/execution", False, str(e))
    
    def test_csv_converter(self):
        """Test CSV Converter skill."""
        print("\n📊 Testing CSV Converter...")
        
        try:
            from csv_converter.main import csv_to_json
            
            # Create test CSV
            test_csv = Path(self.temp_dir) / "test.csv"
            test_csv.write_text("name,age\nAlice,30\nBob,25")
            
            # Convert to JSON
            output_json = Path(self.temp_dir) / "test.json"
            result = csv_to_json(str(test_csv), str(output_json))
            passed = result.get("success") and output_json.exists()
            self.log("CSV Converter", "csv_to_json", passed, f"{result.get('rows', 0)} rows converted")
            
        except Exception as e:
            self.log("CSV Converter", "import/execution", False, str(e))
    
    def test_image_resizer(self):
        """Test Image Resizer skill."""
        print("\n🖼️  Testing Image Resizer...")
        
        try:
            from image_resizer.main import get_image_info
            
            # Create a simple test image
            test_img = Path(self.temp_dir) / "test.png"
            try:
                from PIL import Image
                img = Image.new('RGB', (100, 100), color='red')
                img.save(test_img)
            except:
                self.log("Image Resizer", "pil_not_available", False, "PIL not available for testing")
                return
            
            # Test get info
            result = get_image_info(str(test_img))
            passed = result.get("success") and result.get("width") == 100
            self.log("Image Resizer", "get_image_info", passed, f"{result.get('width')}x{result.get('height')}")
            
        except Exception as e:
            self.log("Image Resizer", "import/execution", False, str(e))
    
    def test_password_generator(self):
        """Test Password Generator skill."""
        print("\n🔐 Testing Password Generator...")
        
        try:
            from password_generator.main import generate_password, check_password_strength
            
            # Test password generation
            password = generate_password(length=16)
            passed = len(password) == 16
            self.log("Password Generator", "generate_password", passed, f"length {len(password)}")
            
            # Test strength check
            result = check_password_strength(password)
            passed = result.get("score", 0) > 0
            self.log("Password Generator", "check_strength", passed, f"score {result.get('score')}/{result.get('max_score')}")
            
        except Exception as e:
            self.log("Password Generator", "import/execution", False, str(e))
    
    def test_markdown_converter(self):
        """Test Markdown Converter skill."""
        print("\n📝 Testing Markdown Converter...")
        
        try:
            from markdown_converter.main import count_markdown_stats
            
            # Create test markdown
            test_md = Path(self.temp_dir) / "test.md"
            test_md.write_text("# Heading\n\nThis is a paragraph with **bold** text.")
            
            # Test stats
            result = count_markdown_stats(str(test_md))
            passed = result.get("success") and result.get("headers") == 1
            self.log("Markdown Converter", "count_stats", passed, f"{result.get('words')} words, {result.get('headers')} headers")
            
        except Exception as e:
            self.log("Markdown Converter", "import/execution", False, str(e))
    
    def run_all_tests(self):
        """Run all skill tests."""
        print("=" * 60)
        print("SMF Works Skills - Test Suite")
        print("=" * 60)
        
        try:
            self.test_file_organizer()
            self.test_pdf_toolkit()
            self.test_text_formatter()
            self.test_qr_generator()
            self.test_system_monitor()
            self.test_website_checker()
            self.test_csv_converter()
            self.test_image_resizer()
            self.test_password_generator()
            self.test_markdown_converter()
        finally:
            self.cleanup()
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        if failed > 0:
            print("\nFailed Tests:")
            for r in self.test_results:
                if not r["passed"]:
                    print(f"  - {r['skill']}: {r['test']}")
        
        return failed == 0


if __name__ == "__main__":
    tester = SkillTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
