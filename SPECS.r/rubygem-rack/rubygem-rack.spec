%global gem_name rack

# There is circular dependency between thin and rack.
%global bootstrap_thin 0

# rubygem-bacon missing for epel7
#  https://bugzilla.redhat.com/show_bug.cgi?id=1138661
%if 0%{?el7}
%global enable_checks 0
%else
%global enable_checks 1
%endif

Name:           rubygem-%{gem_name}
Summary:        Common API for connecting web frameworks, web servers and layers of software
# Introduce Epoch (related to bug 552972)
Epoch:          1
Version:        1.6.2
Release:        1%{?dist}
Group:          Development/Languages
# lib/rack/backports/uri/* are taken from Ruby which is (Ruby or BSD)
# lib/rack/show{status,exceptions}.rb contains snippets from Django under BSD license.
License:        MIT and (Ruby or BSD) and BSD
URL:            http://rack.github.io/
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el6} || 0%{?el7}
Requires:       ruby(rubygems)
Requires:       ruby(release)
%endif
BuildRequires:  ruby
BuildRequires:  rubygems-devel
%if 0%{?enable_checks}
BuildRequires:  rubygem(bacon)
BuildRequires:  memcached
BuildRequires:  rubygem(memcache-client)
%endif
%if 0%{bootstrap_thin} < 1
BuildRequires:  rubygem(thin)
%endif
# Seems that lighttpd test depends on rubygem(fcgi), which is not in Fedora,
# if it will ever be.
#BuildRequires:  lighttpd-fastcgi
BuildArch:      noarch
%if 0%{?fc20} || 0%{?el6} || 0%{?el7}
Provides:       rubygem(%{gem_name}) = %{version}
%endif
Provides:       bundled(okjson) = 20150104

%description
Rack provides a minimal, modular and adaptable interface for developing
web applications in Ruby.  By wrapping HTTP requests and responses in
the simplest way possible, it unifies and distills the API for web
servers, web frameworks, and software in between (the so-called
middleware) into a single method call.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}%{gem_instdir} -type f`; do
    [ ! -z "`head -n 1 $file | grep \"^#!\"`" ] && chmod -v 755 $file
done

%if 0%{?enable_checks}
%check
pushd .%{gem_instdir}

# Get temporary PID file name and start memcached daemon.
PID=%(mktemp)
memcached -d -P "$PID"

bacon -Ilib --automatic --quiet

# Kill memcached daemon.
kill -TERM $(< "$PID")

popd
%endif #end of checks.

%files
%dir %{gem_instdir}
%license %{gem_instdir}/COPYING
%{gem_libdir}
%{gem_instdir}/bin
%{_bindir}/rackup
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/KNOWN-ISSUES
%doc %{gem_instdir}/HISTORY.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/SPEC
%doc %{gem_instdir}/example
%{gem_instdir}/test
%doc %{gem_instdir}/contrib

%changelog
* Wed Jun 17 2015 Vít Ondruch <vondruch@redhat.com> - 1:1.6.2-1
- Update to Rack 1.6.2.

* Tue Jun 2 2015 Steve Traylen <jstribny@redhat.com> - 1:1.6.1-1
- Update to 1.6.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:1.6.0-1
- Update to 1.6.0

* Thu Sep 25 2014 Steve Traylen <steve.traylen@cern.ch> - 1:1.5.2-4
- Add enable_check flag and disable check for .el7.
- Rely on autorequires and autoprovides.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 05 2014  Josef Stribny <jstribny@redhat.com> - 1:1.5.2-2
- Fix licensing
- Add virtual provide for bundled okjson

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 1:1.5.2-1
- Update to rack 1.5.2

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-3
- Enable thin test suite.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.5-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 08 2013 Josef Stribny <jstribny@redhat.com> - 1:1.4.5-1
- Update to Rack 1.4.5.

* Tue Jan 15 2013 Vít Ondruch <vondruch@redhat.com> - 1:1.4.4-1
- Update to Rack 1.4.4.

* Thu Nov 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-2
- Fixed epoch in -doc sub-package.

* Mon Oct 29 2012 Vít Ondruch <vondruch@redhat.com> - 1:1.4.1-1
- Update to Rack 1.4.1.
- Documentation moved into subpackage.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-2
- Rebuilt for Ruby 1.9.3.

* Thu Jan 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:1.4.0-1
- Update to Rack 1.4.
- Moved gem install to %%prep to be able to apply patches.
- Applied two patches that fix test failures with Ruby 1.8.7-p357.

* Tue Jun 28 2011 Vít Ondruch <vondruch@redhat.com> - 1:1.3.0-1
- Updated to Rack 1.3.
- Fixed FTBFS.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.1.0-2
- Epoch 1 for keeping upgrade path from F-12 (related to bug 552972)
- Enable %%check

* Mon Jan  4 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.1.0-1
- New upstream version

* Sun Oct 25 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.0.1-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 26 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.0.0-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.9.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-2
- Remove unused macro (#470694)
- Add ruby(abi) = 1.8 as required by package guidelines (#470694)
- Move %%{gem_dir}/bin/rackup to %%{_bindir} (#470694)

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-1
- Initial package
