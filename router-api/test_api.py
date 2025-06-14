#!/usr/bin/env python3

import requests
import json
import time
import sys

# API base URL
BASE_URL = "http://localhost:8080"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_agent_selection():
    """Test the agent selection endpoint"""
    print("\nTesting agent selection...")
    
    test_cases = [
        {
            "text": "Write a Python script to check network connectivity",
            "expected_agent": "code"
        },
        {
            "text": "Find a file called report.pdf on my drive",
            "expected_agent": "files"
        },
        {
            "text": "Search the web for the latest AI news",
            "expected_agent": "web"
        },
        {
            "text": "Hello, how are you?",
            "expected_agent": "talk"
        }
    ]
    
    success_count = 0
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/select-agent",
                json={"text": test_case["text"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i} passed")
                print(f"   Query: {test_case['text']}")
                print(f"   Selected: {result['selected_agent']} ({result['agent_name']})")
                print(f"   Complexity: {result['complexity']}")
                print(f"   Language: {result['language_detected']}")
                success_count += 1
            else:
                print(f"❌ Test {i} failed with status {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
    
    return success_count == len(test_cases)

def test_complexity_estimation():
    """Test the complexity estimation endpoint"""
    print("\nTesting complexity estimation...")
    
    test_cases = [
        {
            "text": "Hi there!",
            "expected_complexity": "LOW"
        },
        {
            "text": "Create a machine learning model to predict stock prices and deploy it as a web service",
            "expected_complexity": "HIGH"
        }
    ]
    
    success_count = 0
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/estimate-complexity",
                json={"text": test_case["text"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i} passed")
                print(f"   Query: {test_case['text']}")
                print(f"   Complexity: {result['complexity']}")
                print(f"   Confidence: {result['confidence']}")
                success_count += 1
            else:
                print(f"❌ Test {i} failed with status {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
    
    return success_count == len(test_cases)

def test_list_agents():
    """Test the list agents endpoint"""
    print("\nTesting list agents...")
    try:
        response = requests.get(f"{BASE_URL}/agents")
        if response.status_code == 200:
            result = response.json()
            print("✅ List agents passed")
            print(f"   Available agents: {len(result['agents'])}")
            for agent in result['agents']:
                print(f"   - {agent['name']} ({agent['type']}) - {agent['role']}")
            return True
        else:
            print(f"❌ List agents failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ List agents failed: {e}")
        return False

def wait_for_service():
    """Wait for the service to be ready"""
    print("Waiting for service to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("Service is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_attempts - 1:
            print(f"Attempt {attempt + 1}/{max_attempts}, waiting...")
            time.sleep(2)
    
    print("Service is not responding after maximum attempts")
    return False

def main():
    """Main test function"""
    print("🚀 AgentRouter API Test Suite")
    print("=" * 40)
    
    # Wait for service to be ready
    if not wait_for_service():
        print("❌ Service is not available. Make sure it's running.")
        sys.exit(1)
    
    # Run all tests
    tests = [
        test_health_check,
        test_agent_selection,
        test_complexity_estimation,
        test_list_agents
    ]
    
    passed_tests = 0
    for test in tests:
        if test():
            passed_tests += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed_tests}/{len(tests)} tests passed")
    
    if passed_tests == len(tests):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 