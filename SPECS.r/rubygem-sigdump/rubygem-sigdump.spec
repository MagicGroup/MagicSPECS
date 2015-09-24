# Generated from sigdump-0.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sigdump

Name: rubygem-%{gem_name}
Version: 0.2.2
Release: 1%{?dist}
Summary: Ruby signal handler which dumps running threads and number of allocated objects
License: MIT
URL: https://github.com/frsyuki/sigdump
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
%if 0%{?fedora} <= 20 || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Setup signal handler which dumps backtrace of running threads and number of
allocated objects per class. Require 'sigdump/setup', send SIGCONT, and see
/tmp/sigdump-<pid>.log.


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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/.gitignore

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.2.2-1
- Initial package
