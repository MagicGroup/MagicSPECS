Name:           libqb
Version: 0.17.2
Release: 3%{?dist}
Summary:        An IPC library for high performance servers
Summary(zh_CN.UTF-8): 高性能服务的 IPC 库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.libqb.org
Source0:        https://fedorahosted.org/releases/q/u/quarterback/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool doxygen procps check-devel automake

#Requires: <nothing>

%description
libqb provides high performance client server reusable features.
Initially these are IPC and poll.

%description -l zh_CN.UTF-8
高性能服务的 IPC 库。

%prep
%setup -q

# work-around for broken epoll in rawhide/f17
%build
%configure --disable-static ac_cv_func_epoll_create1=no ac_cv_func_epoll_create=no
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT/%{_docdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/qb-blackbox
%{_libdir}/libqb.so.*

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%defattr(-,root,root,-)
%doc COPYING README.markdown
%{_includedir}/qb/
%{_libdir}/libqb.so
%{_libdir}/pkgconfig/libqb.pc
%{_mandir}/man3/qb*3*
%{_mandir}/man8/qb-blackbox.8.gz

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.17.2-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.17.2-2
- 更新到 0.17.2

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 0.17.0-1
- 更新到 0.17.0


* Mon Oct 29 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.3-2
Fix test code highlighted by new check version
Remove the call to autogen.sh - not needed anymore.

* Mon Oct 29 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.3-1
IPC: Pass the timeout to poll() if the recv function returns EAGAIN
LOG: make the format comparison safe and sane
LOG: don't break on empty callsites, just ignore them
LOG: use the array callback to register new callsites
array: add a mechanism to get a callback when a bin is allocated
Solaris based operating systems don't define MSG_NOSIGNAL and SO_NOSIGPIPE.
Make sure atomic's are initialized (for non-gcc atomic).

* Wed Sep 12 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.2-2
Fix a crash in ptrie if you iterate over the map in the deleted notifier.

* Mon Sep 10 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.2-1
Get libqb building on cygwin.
ipc_us: slightly more robust cmsg handling
ipc_us: on Linux, set SO_PASSCRED on the sending socket too
ipc_us: clear request unused fields
TEST: Include writing and reading the blackbox in the log_long_msg test
LOG: fix qb_vsnprintf_deserialize()
blackbox: fix 64-bit big-endian issues
Remove IPC_NEEDS_RESPONSE_ACK and turn off shm ipc on solaris
Define unix path max for openbsd
Only turn on ipc_needs_response_ack=yes for solaris
Some improvements to kqueue usage.
kqueue: drop log message to trace.
Fix splint warning
openbsd requires netinet/in.h before arpa/inet.h
Avoid strcpy() use strlcpy() instead.
Fix kqueue complile warnings
openbsd doesn't have EBADMSG
openbsd has a different UNIX_PATH_MAX
LOG: change qb_vsprintf_serialize() into qb_vsnprintf_serialize()
TEST: increase timeout to 6 secs as the recv timeout is 5 secs
TEST: get the logic right - grrr.
Turn off attribute_section on netbsd
Some missing pshared semaphore checks
Cleanup the checks for pshared semaphores
Add a config check for pthread_mutexattr_setpshared
Remove uses of timersub and use qb_util_stopwatch
RB: change the #error to ENOTSUP if no usable shared process sem
LOOP-KQUEUE: fix reference before assignment.
build: fix libqb.pc creation and make maintainer-clean
LOG: Make sure the semaphores are initialized.
build: remove bashism in cc support check
Catch disconnected sockets on Solaris
Don't free rb->shared_hdr in qb_rb_create_from_file()
Check error return of qb_ipcs_uc_recv_and_auth()
Fix removal of automatically installed doc files when building rpms
Add the mailing list to the travis email notifications.
Work around debian not setting the arch path in splint.
Remove color-tests and parallel-tests automake options.
Add travis continuous integration config
LOG: Invoke custom log filter function if tag changes
tests/rbwriter: don't ignore write failure
ipcs: avoid use-after-free for size-0 || disconnect-request

* Wed Jul 18 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.1-1
RB: set the new read pointer after clearing the header (#839605).
RB: improve the debug print outs
RB: be more explicit about the word alignment
RB: cleanup the macros for wrapping the index
RB: use sem_getvalue as a tie breaker when read_pt == write_pt
RB: if read or peek don't get the message then re-post to the semaphore
RB: convert the rb_peek() status into a recv like status.
RB: use internal reclaim function
IPC: use calloc instead of malloc to fix valgrind warnings
Upgrade the doxygen config.
Fix a valgrind error.

* Sun Jun 24 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.0-1
LOG: fix threaded logging.
Add user control of the permissions that are set on the shared mem files
LOG: Restrict string trucation during serialization to when a precision is specified
LOG: Gracefully fail when the caller exceeds QB_LOG_MAX_LEN
LOG: Observe field widths when serializing string arguments
RB: use the same mechanism in reclaim as read/peek to detect end-of-ring
Add needs_response_ack option to ./check
RB: fix wrong sem_flg IPC_NOWAIT option
TESTS: fix warning about unused functions
Remove D_FORTIFY_SOURCE from check.
Open shared mem file in /dev/shm only for linux
Don't use msg_flags on solaris (recvmsg).
Turn off attribute_section on solaris
ipc example: add -e (events) option
IPC: if the server returns EAGAIN or ETIMEOUT the check the connection
LOG: make it possible to fsync() on each file log.
IPC: make sure that the created callback happens before dispatches
LOG: fix the printing of %p in the blackbox
IPC: On bsd's use the notifier for responses
IPC: interpret ECONNRESET and EPIPE as ENOTCONN
cleanup some warnings
config: use newer AC_COMPILE_IFELSE()
blackbox: fix %p formatting
LOG: put all fields in the blackbox (added priority and tags)
example: make the priority uint8_t
Remove strerror out of check_funcs
RB: fix compiler warning.
Add replacement function stpcpy
Add missing AC_TYPE_UINT16_T to configure.ac
Use AC_FUNC_STRERROR_R and STRERROR_R_CHAR_P
Add stpcpy strcasecmp to the check_funcs
Move some conditional defines into code (from the configure script)
Remove some unused configure checks
Remove message queues
Check for union semun properly
Blackbox: provide more space for log messages when reading from the blackbox.
Add the blackbox reader manpage to the spec file
Enable error logging for the blackbox reader
RB: Read the file size into an initialized variable of the correct size
Add a tool to dump the blackbox.
RB: to be safer save the read and write pointers at the top of the blackbox
avoid unwarranted use of strncpy: use memcpy instead
blackbox: fix the print_from_file()
RB: add an option to not use any semaphores
LOG: tweak the blackbox format string
LOG: accept NULL strings into the blackbox
LOG: protect close and reload from calling log
Add benchmark option (-b) to examples/ipcclient
TEST: make rbreader/writer more like the other benchmarking apps
IPC: log the connection description in all logs
TEST: re-organise the ipc test suites
IPC: only modify the dispatch if we get EAGAIN
Correctly display timestamp in blackbox

* Thu May 10 2012 Angus Salkeld <asalkeld@redhat.com> - 0.13.0-1
- Remove unneccessary __attribute__ ((aligned(8))) from internal headers
- IPC: add a new function to get (and alloc) the extended stats.
- Revert "Add the event queue length to the connection stats."
- IPC: cleanup better on a failed client connect.
- IPC(soc): be more consistent with control struct size
- IPC: kill a compiler warning
- IPC(soc): pass in the correct size into munmap()
- TEST: Use /bin/sh not /bin/bash
- TEST: check for lost shared mem on bsd too
- rb: cleanup the semaphores
- Fix some small issues in ./check
- Cleanup the .gitignore files
- configure.ac tweaks
- Remove HZ and use sysconf instead.
- SUN_LEN() macro is present if __EXTENSIONS__ is defined on Illumos
- PF_UNIX is a POSIX standard name
- Test for log facility names
- IPC: drop log message to debug.
- IPC: fix retrying of partial recv's and sends.
- IPC: initialize enough shared mem for all 3 one way connections.
- IPC: keep retrying to recv the socket message if partially recv'ed (part 2)
- IPC: keep retrying to recv the socket message if partially recv'ed
- IPC: handle the server shutdown better
- IPC: handle a connection disconnect from the server better
- IPC: make it possible to send events in the connected callback.
- Add the event queue length to the connection stats.
- IPC: add a is_connected client side function.
- Fix typo in ./check
- docs: clarify the need to use request/response headers
- Remove unused local variable
- IPC: change the socket recv function to read the response header.
- Add some special commands into the ipc example
- TEST: improve the tracing in the ipc tests.
- Make "make (s)rpm" work more reliably
- TEST: add a test to confirm we get the events we send.
- TEST: reuse send_and_check for events.
- IPC: make it possible for a root client to talk to a non-root server.
- Run ./Lindent in the examples directory
- Add some debug code to the ipcclient example
- IPC: make sure ipc (socket) clients can connect to a server running as root.
- IPC: allow qb to bump the max_message_size
- IPC: check for a sane minimum max_message_size
- add rpl_sem.h loop_poll_int.h to noinst_headers
- Handle errors more consistently
- call recv_ready on socket types
- Handle a recv of size 0
- make bsd shm path better by default.
- Fix kqueue on freebsd.
- Get the example socket includes right.
- Fix kqueue compiling.
- POLL: seperate out the poll/epoll and add kqueue
- Test existence of getpeer* functions
- Add inet header to tcpclient example
- Don't link with setpshared if unavailable
- NetBSD doesn't have semun defined
- Use MADV_NOSYNC only on systems where available
- Use SCHED_BATCH only on platforms where available
- Fix a bug introduced by the bsd patch.
- Cleanup the selection of semaphores to use
- Fix some leaks in the logging.
- Try and improve the portability on bsd variants.

* Sun Mar 11 2012  Angus Salkeld <asalkeld@redhat.com> - 0.11.1-1
- configue libqb to not use epoll as it seems broken (#800865)
- LOOP: remove some old timerfd code.
- TEST: add a test to check the order of the jobs
- LOOP: when new jobs are added they are added to the head instead of the tail.
- LOG: Now the array is self locking we can make the lookup array dynamic
- Add locking to the array when growing.
- IPC: make the _request_q_len_get() function more obvious.
- IPC: fix multiple receives from qb_ipc_us_recv()
- IPC: make sure that the wrong union member is not written to.
- TIMER: check for null timer handle

Wed Mar 7 2012  Angus Salkeld <asalkeld@redhat.com> - 0.11.0-1
- ARRAY: cleanup the pointer sizeof()
- LOG: turn off __attribute__(section) for powerpc (not working)
- TESTS: move the util tests into "slow-tests" (i.e. optional)
- TEST: make the test_priority the same type as in the callsite
- LOG: make the log arrays manually grow-able since we need to lock the calls.
- RB: fix test failure on ppc
- RB: change the name of the size to word_size to be more clear
- TEST: add some more signal tests.
- LOOP: fix deletion of signal handlers when they are pending
- LOOP: signal handlers were always added as high priority.
- TEST: deal with mac's limited sed
- check: add debugging to the configure options and remove unused options
- TEST: properly clear the filters
- LOG: expose the mechanism to get a dynamic callsite.
- Revert part of my COARSE grained timer commit
- Remove timerfd usage and go back to timelist.
- UTIL: if possible use COARSE resolution clocks - they are much faster.
- ARRAY: save memory (in the bins array) and allow holes in the array
- LOOP: add qb_loop_timer_is_running()
- LOOP: allow stop() and run() to be called with NULL loop instance.
- LOOP: fix doxygen parameter comment
- LOG: add stdout target
- LOOP: add a function to delete jobs
- LOG: remove debug printf's
- LOG: remove an old/incorrect doxygen comment.
- LOG: add a hostname %H format specifier.
- LOG: Add qb_log_filter_fn_set()

* Tue Feb 14 2012 Angus Salkeld <asalkeld@redhat.com> - 0.10.1-1
- Fix "make distcheck" add include path to AM_CPPFLAGS
- Bump the version to 0.10.1
- clang: Remove unused code
- TEST: make the ipc failure test closer to corosync's case.
- RB: add a debug message if trying to read a message of the wrong size
- IPC: split up the recv into chuncks of 2 seconds. (#788742)
- Be more consistent with the internal logs.
- LOOP: make it possible to pass in NULL as the default loop instance
- RB: use the proper struct not the typedef in the implementation.
- RB: Fix potential mem leak
- Don't mix enums (QB_TRUE/TRUE)
- use random() not rand()
- Remove dead code
- set umask before calling mkstemp()
- Use safer versions of string functions (strcpy -> strlcpy)
- Increase the coverity aggressiveness
- TEST: make the loop ratelimit test more forgiving.

* Tue Feb 07 2012 Angus Salkeld <asalkeld@redhat.com> - 0.10.0-1
- LOOP: handle errors from the poll function
- LOOP: make the item type applicable to jobs too.
- LOOP: fix the todo calculations.
- TEST: check for a single job causing a cpu spin
- LOOP: prevent jobs from consuming too much cpu.
- Get coverity to ignore this warning.
- Change example code to use fgets instead of gets
- LOG: pass the result of qb_log_thread_start() back to the user
- Fix some issues found by clang
- Add clang-analyzer check
- Add a split timer to the stopwatch.
- IPC: merge common code into new function
- IPC: better handle a disconnect been called from within connection_created()
- IPC: fix scary typo
- IPC: fix server error handling

* Mon Feb 06 2012 Angus Salkeld <asalkeld@redhat.com> - 0.9.0-2
- Fix a spin in the mainloop when a timer or poll gets removed
  When in the job queue (#787196).

* Fri Jan 27 2012  Angus Salkeld <asalkeld@redhat.com> - 0.9.0-1
- Rebased to 0.9.0

* Tue Jan 10 2012  Angus Salkeld <asalkeld@redhat.com> - 0.8.1-2
- fix qb_timespec_add_ms()

* Thu Jan 5 2012  Angus Salkeld <asalkeld@redhat.com> - 0.8.1-1
- Rebased to 0.8.1 (#771914)

* Wed Nov 17 2011 Angus Salkeld <asalkeld@redhat.com> - 0.7.0-1
- Rebased to 0.7.0 (#754610)

* Thu Sep 1 2011 Angus Salkeld <asalkeld@redhat.com> - 0.6.0-2
- LOG: fix the default syslog filter

* Tue Aug 30 2011 Angus Salkeld <asalkeld@redhat.com> - 0.6.0-1
- Rebased to 0.6.0 which includes (#734457):
- Add a stop watch
- LOG: serialize the va_list, don't snprintf
- LOG: change active list into array access
- atomic: fix qb_atomic_pointer macros
- LOG: allow the thread priority to be set.
- Fix splint warning on ubuntu 11.04

* Mon Jul 18 2011 Angus Salkeld <asalkeld@redhat.com> - 0.5.1-1
- Rebased to 0.5.1 which includes:
- LOOP: make the return more consistent in qb_loop_timer_expire_time_get()
- LOG: add string.h to qblog.h
- Add a qb_strerror_r wrapper.
- don't let an invalid time stamp provoke a NULL dereference
- LOG: move priority check up to prevent unnecessary format.
- rename README to README.markdown

* Wed Jun 8 2011 Angus Salkeld <asalkeld@redhat.com> - 0.5.0-1
- Rebased to 0.5.0 which includes:
- new logging API
- support for sparc
- coverity fixes

* Tue Feb 8 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.1-2
- SPEC: improve devel files section
- SPEC: remove global variables

* Mon Jan 31 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.1-1
- SPEC: add procps to BuildRequire
- SPEC: remove automake and autoconf from BuildRequire
- SPEC: remove call to ./autogen.sh
- SPEC: update to new upstream version 0.4.1
- LOOP: check read() return value
- DOCS: add missing @param on new timeout argument
- BUILD: only set -g and -O options if explicitly requested.
- BUILD: Remove unneccessary check for library "dl"
- BUILD: improve the release build system

* Fri Jan 14 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.0-2
- remove "." from Summary
- Add "check-devel to BuildRequires
- Add "make check" to check section
- Changed a buildroot to RPM_BUILD_ROOT
- Document alphatag, numcomm and dirty variables.

* Sun Jan 09 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.0-1
- Initial release
