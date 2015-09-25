%global gem_name ghost

Summary:        Allows you to create, list, and modify local hostnames
Name:           rubygem-%{gem_name}
Version:        0.3.0
Release:        9%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://github.com/bjeanes/ghost
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(release) >= 1.9.1
Requires:       ruby(rubygems)
BuildRequires:  rubygems-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
This gem is designed primarily for web developers who need to add
and modify hostnames to their system for virtual hosts on their
local/remote web server. However, it could be of use to other people
who would otherwise modify their `/etc/hosts` file manually and
flush the cache.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T -n %{gem_name}-%{version}
mkdir -p .%{gem_dir}

%build


%install
gem install --local --install-dir .%{gem_dir} \
        -V \
        --force \
        --rdoc \
        %{SOURCE0}

install -d -m0755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m0755 $RPM_BUILD_ROOT/%{gem_dir}

cp -a .%{gem_dir}/* $RPM_BUILD_ROOT%{gem_dir}/

mv $RPM_BUILD_ROOT%{gem_dir}/bin/* $RPM_BUILD_ROOT/%{_bindir}
rmdir $RPM_BUILD_ROOT%{gem_dir}/bin
find $RPM_BUILD_ROOT%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove zero-length documentation files
find $RPM_BUILD_ROOT%{gem_docdir} -empty -delete
find $RPM_BUILD_ROOT%{gem_instdir} -maxdepth 1 -empty -delete


%files
%dir %{gem_instdir}
%{_bindir}/ghost
%{_bindir}/ghost-ssh
%{gem_instdir}/bin
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}

%files doc
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.0-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 17 2013 Matt Spaulding <mspaulding06@gmail.com> - 0.3.0-5
- Misunderstood what fix was needed. Changed ruby(abi) to ruby(release)

* Sat Mar 16 2013 Matt Spaulding <mspaulding06@gmail.com> - 0.3.0-4
- Updated ruby(abi) to 1.9.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 13 2012 Matt Spaulding <mspaulding06@gmail.com> - 0.3.0-2
- Updated prep section
- Excluded gem cache
- Added -doc package
- Removed clean section

* Thu Jul 5 2012 Matt Spaulding <mspaulding06@gmail.com> - 0.3.0-1
- Initial build

