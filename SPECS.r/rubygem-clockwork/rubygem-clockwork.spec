# Generated from clockwork-0.7.7.gem by gem2rpm -*- rpm-spec -*-
%global gem_name clockwork

Name: rubygem-%{gem_name}
Version: 0.7.7
Release: 4%{?dist}
Summary: A scheduler process to replace cron
Group: Development/Languages
License: MIT
URL: http://github.com/tomykaira/clockwork
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# wget https://raw.githubusercontent.com/tomykaira/clockwork/master/clockworkd.1
Source1: clockworkd.1
# wget https://raw.githubusercontent.com/tomykaira/clockwork/master/LICENSE
Source2: LICENSE
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
# contest is for test/unit and not in Fedora
# BuildRequires: rubygem(daemons) 
# BuildRequires: rubygem(contest)
# BuildRequires: rubygem(minitest) => 4.0
# BuildRequires: rubygem(minitest) < 5
# BuildRequires: rubygem(mocha)
BuildArch: noarch

%description
A scheduler process to replace cron, using a more flexible Ruby syntax running
as a single long-running process.  Inspired by rufus-scheduler and
resque-scheduler.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Install man pages into appropriate place
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1

# License
install -m 0644 %{SOURCE2} %{buildroot}%{gem_instdir}/

# contest is for test/unit and not in Fedora
#%%check

%files
%dir %{gem_instdir}
%{_bindir}/clockwork
%{_bindir}/clockworkd
%{gem_instdir}/bin
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%doc %{_mandir}/man1/clockworkd.1*
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/example.rb

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 0.7.7-3
- Include LICENSE file
- Drop support for f20

* Fri Aug 22 2014 Josef Stribny <jstribny@redhat.com> - 0.7.7-2
- Add man page

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.7.7-1
- Initial package
