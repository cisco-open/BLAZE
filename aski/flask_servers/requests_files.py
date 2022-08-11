"""

dataset/file-related

    1) GET/files/all_files - all available files (datasets/strings)
        - Input: {}
        - Output: {"datasets": {"name": [str]}}
        - Use Case: Generate that dropdown for the dash 
        - Who's Doing: Thomas

    2) GET/files/file - specific file text (details) 
        - Input: {"file": str}
        - Output: {"file": str, "content": str, "content-length": int}
        - Use Case: Show preview for files
        - Who's Doing: Jason

    3) POST/files/initialize - initialize datasets 
        - Input: {"datasets": [str]}
        - Output: {}
        - Use Case: if user chooses squad + cnn dailymail in yaml
        - Who's Doing: Advit

    4) POST/files/upload - user uploads file 
        - Input: {"file": str, "content": str}
        - Output: {}
        - Use Case: when the user uploads a file
        - Who's Doing: Jason

    5) DELETE/files/upload - user deletes file
        - Input: {"file": str}
        - Output: {}
        - Use Case: when the user deletes a **CUSTOM** file
        - Who's Doing: Jason


"""