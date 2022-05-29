#include <chrono>
#include <cmath>
#include <iostream>
#include <queue>
#include <random>
#include <thread>
#include <vector>
#include <mutex>
#include <condition_variable>

using namespace std;

/**
 * Semaphore class
 */
class Semaphore {

    public:
        /**
         * Constructor
         *
         * @param counter The starting value
         */
        explicit Semaphore(const string & name, int counter = 0) {
            this->_name = name;
            this->_counter = counter;
        }
        virtual ~Semaphore() = default;

        /**
         * Attempt to enter the critical region. Wait if it is closed.
         */
        void down() {
            // Wrap the mutex and kLockMutex
            unique_lock<mutex> lock(_mutex);

            // Wait for the kLockMutex to be released (coping with spurious wake-ups)
            while (!_counter) {
                printf("Semaphore blocked: %s\n", this->_name.c_str());
                cout << std::flush;
                _condition.wait(lock);
            }

            // Update the counter
            _counter--;

            // The mutex is automatically unlocked
        }

        /**
         * Attempt to enter the critical region. Skip if it is closed.
         *
         * @return True if entered in the region
         */
        bool tryDown() {
            // Wrap the mutex and kLockMutex
            std::lock_guard<mutex> lock(_mutex);

            // Check if the thread can enter the critical region
            bool can_enter = _counter > 0;
            if (can_enter) {

                // Update the counter
                _counter--;
            }

            return can_enter;

            // The mutex is automatically unlocked
        }

        /**
         * Notify it is exiting the critical region.
         */
        void up() {
            // Wrap the mutex and kLockMutex
            std::lock_guard<mutex> lock(_mutex);

            // Update the counter
            _counter++;

            // Notify the condition was changed
            _condition.notify_one();

            // The mutex is automatically unlocked
        }

    private:
        mutex _mutex;
        condition_variable _condition;
        int _counter = 0;
        string _name;
};
