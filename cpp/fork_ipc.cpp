#include <iostream>
#include <string>
#include <fstream>
#include <unistd.h>
#include <thread>
#include <sys/types.h>
#include <sys/wait.h>

/**
 * sample code to learn IPC in c++
 * Fork to create a child process.
 * Child reads from stdin and writes to stdout as if it is a separate process.
 * However we attach pipes to child's stdin and stdout, where parent can control the child's stdin and stdout.
 * This was created for a tool (pigz) where it is not thread safe and we need to fork and exec it in a separate process.
 *
 * To compile: g++  fork_ipc.cpp
 * To run: echo -e "Ping\nHello" | ./a.out
 */


int child_process(int stdin_fd[2], int stdout_fd[2]) {
    /**
     * Child process function. Reads from stdin and writes to stdout.
     * If the input is "Ping", it writes "Pong" to stdout. Otherwise, it writes "Error".
     *
     * @param stdin_fd: File descriptors for the input pipe
     * @param stdout_fd: File descriptors for the output pipe
     * @return: 0 on success
     */
    // 0 : read; 1:write
    // bind read end of pipe to STDIN; close the write end
    dup2(stdin_fd[0], STDIN_FILENO);
    close(stdin_fd[1]);

    // close the read end of STDOUT and bind the write end
    close(stdout_fd[0]);
    dup2(stdout_fd[1], STDOUT_FILENO);

    // read line by line from stdin and write to stdout

    for (std::string line; std::getline(std::cin, line);) {
        std::cout << "Child received: " << line << std::endl;
        if (line == "Ping") {
            std::cout << "Child sending: Pong" << std::endl;
        } else {
            std::cout << "Child sending: Error" << std::endl;
        }
    }
    // flush the output stream
    std::cout << std::flush;
    // close the output stream
    close(stdout_fd[1]);
    return 0;
}


// Function to handle parent process
int parent_process_debug(int in_fd[2], int out_fd[2]) {

    // 0: read; 1:write
    close(in_fd[0]);  // read end
    int inp_write_end = in_fd[1]; // write end

    int out_read_end = out_fd[0];  // read end
    close(out_fd[1]);  // write end


    // Write "Ping" to the pipe
    std::string message = "Ping\n";
    write(inp_write_end, message.c_str(), message.size());

    // Write "blah" to the pipe
    message = "blah\n";
    write(inp_write_end, message.c_str(), message.size());

    close(inp_write_end);
    wait(nullptr); // Wait for child process to exit

    FILE* pipe_read = fdopen(out_read_end, "r");
    if (!pipe_read) {
        perror("Error opening pipe for reading");
        exit(1);
    }

    char* line = nullptr;
    size_t len = 0;
    ssize_t bytes_read;

    // Read line by line until STDIN is closed
    while ((bytes_read = getline(&line, &len, pipe_read)) != -1) {
        std::string message(line, bytes_read - 1); // Exclude newline
        std::cout << "Parent received: " << message << std::endl;
    }
    //std::cout << "Parent process finished reading: " << bytes_read << std::endl;
    free(line);
    fclose(pipe_read);
    return 0;
}


void copy_stream(int in_fd, int out_fd) {
    /**
     * Copy data from input file descriptor to output file descriptor
     * @param in_fd: Input file descriptor
     * @param out_fd: Output file descriptor
     */
    int buffer_size = 1024;
    char buffer[buffer_size];
    ssize_t bytes_read;
    while ((bytes_read = read(in_fd, buffer, sizeof(buffer))) > 0) {
        write(out_fd, buffer, bytes_read);
    }
    close(in_fd);
    close(out_fd);
}

int parent_glue_io(int in_fd[2], int out_fd[2]) {
    /**
     * Glue the parent process's stdin/stdout to the child process's stdin/stdout
     * @param in_fd: File descriptors for the input pipe
     * @param out_fd: File descriptors for the output pipe
     */
    // Close unnecessary pipe ends
    close(in_fd[0]);  // Close read end of input pipe
    close(out_fd[1]); // Close write end of output pipe

    // Create threads to copy data between pipes and stdin/stdout
    std::thread t1(copy_stream, STDIN_FILENO, in_fd[1]);  // Copy input pipe to stdin
    std::thread t2(copy_stream, out_fd[0], STDOUT_FILENO); // Copy stdout to output pipe

    // Wait for threads to finish
    t1.join();
    t2.join();

    // Wait for child process to exit
    wait(nullptr);

    return 0;
}

int main() {
    int stdin_fd[2];
    int stdout_fd[2];
    pid_t child_pid;
    bool debug = false;

    // Create the pipe
    if (pipe(stdin_fd) == -1 || pipe(stdout_fd) == -1) {
        perror("Error creating pipes");
        return 1;
    }

    // Fork a child process
    child_pid = fork();
    int status;
    if (child_pid == -1) {
        perror("Error forking process");
        return 1;
    }
    if (child_pid == 0) { // Child process
        return child_process(stdin_fd, stdout_fd);
    } else { // Parent process
        if (debug) {
            return parent_process_debug(stdin_fd, stdout_fd);
        } else { // Glue stdin and stdout to child process
            std::cerr << "Parent process is biding stdin and stdout to child. use pipes to pass data\n";
            return parent_glue_io(stdin_fd, stdout_fd);
        }
    }
}
