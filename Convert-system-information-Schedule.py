import os
import csv
from datetime import datetime
import time
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def get_latest_date(csv_file_path):
    try:
        latest_date = None
        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:  # Empty row will evaluate to False
                        latest_date = row[0]
            return latest_date
    except Exception as e:
        print(f"Error getting latest date: {e}")
        return None

def get_cpu_info():
    try:
        cpu_info = os.popen("wmic cpu get loadpercentage").read().strip().split('\n')[1:]
        cpu_usage = [int(info) for info in cpu_info if info.strip()]
        return cpu_usage
    except Exception as e:
        print(f"Error getting CPU info: {e}")
        return []

def get_memory_info():
    try:
        memory = psutil.virtual_memory()
        memory_total_gb = round(memory.total / (1024 ** 3), 2)
        memory_available_gb = round(memory.available / (1024 ** 3), 2)
        return memory_total_gb, memory_available_gb
    except Exception as e:
        print(f"Error getting memory info: {e}")
        return None, None

def get_disk_info():
    try:
        disk_info = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # Skip inaccessible drives
                continue
            device = partition.device
            freespace_gb = round(usage.free / (1024 * 1024 * 1024), 2)
            size_gb = round(usage.total / (1024 * 1024 * 1024), 2)
            disk_info.append((device, freespace_gb, size_gb))
        return disk_info
    except Exception as e:
        print(f"Error getting disk info: {e}")
        return []

def write_to_csv(cpu_info, memory_info, disk_info, latest_date):
    try:
        desktop_path = get_desktop_path()
        output_file_path = os.path.join(desktop_path, "系統資訊.csv")

        today_date = datetime.now().strftime("%Y-%m-%d,%H:%M")

        with open(output_file_path, "r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            existing_data = list(reader)

        # Check if the row already exists, if not, write the new row to the CSV file
        new_row = [today_date, cpu_info[0], memory_info[0], memory_info[1]]
        new_row += [f"{disk[1]} ({disk[2]})" for disk in disk_info]  # Add disk info
        if new_row not in existing_data:
            with open(output_file_path, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not existing_data:  # If file is empty, write header
                    writer.writerow(["Date", "CPU Usage (%)", "Memory Total (GB)", "Memory Available (GB)"] + 
                                    [f"Disk {i} Free Space (GB) (Total Space GB)" for i in range(1, len(disk_info) + 1)])
                writer.writerow(new_row)

        return output_file_path
    except PermissionError as pe:
        print(f"Permission denied: {pe}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return None

def send_email(receiver_email):
    try:
        sender_email = "###@###"  # Change this to your email
        password = "###"  # Change this to your email password

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "System Information Report"

        body = "The system information report has been generated successfully."
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("###", 25)  # Change this to your SMTP server and port
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    try:
        print("開始執行..請稍等...")
        desktop_path = get_desktop_path()
        output_file_path = os.path.join(desktop_path, "系統資訊.csv")
        
        # 檢查CSV文件是否存在，如果不存在，則寫入標題行
        if not os.path.exists(output_file_path):
            with open(output_file_path, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Date", "CPU Usage (%)", "Memory Total (GB)", "Memory Available (GB)"])
        
        print("取得時間資訊....")
        print("取得CPU資訊....")
        cpu_info = get_cpu_info()
        print("取得記憶體資訊....")
        memory_info = get_memory_info()
        print("取得硬碟資訊....")
        disk_info = get_disk_info()
        print("開始寫入....")
        output_file_path = write_to_csv(cpu_info, memory_info, disk_info, None)
        if output_file_path:
            if os.path.exists(output_file_path):
                print("成功寫入資料到CSV文件。")
                send_email("###@###")  # 寫入CSV後發送郵件
            else:
                print("寫入資料到CSV文件失敗。")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("程序已啟動，等待定時任務執行...")

# Execute main() once immediately
main()

# 定時執行主函式，每天中午執行一次
schedule.every().day.at("14:14").do(main)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")