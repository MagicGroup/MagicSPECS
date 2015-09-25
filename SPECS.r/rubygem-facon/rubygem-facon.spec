%global gem_name facon

Summary: Tiny mocking library
Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 9%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/chuyeow/facon/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
Requires: rubygem(bacon)
BuildRequires: rubygems-devel
BuildRequires: rubygem(bacon)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A mocking library in the spirit of the Bacon spec library. Small, compact, and
works with Bacon.

%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Requires:          %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/Gemfile.lock
rm -f %{buildroot}%{gem_instdir}/Gemfile
pushd %{buildroot}%{gem_instdir}
sed -i -e 's|require "bundler"||' spec/spec_helper.rb
sed -i -e 's|Bundler.setup||' spec/spec_helper.rb



%clean
rm -rf %{buildroot}

%check
pushd %{buildroot}%{gem_instdir}
bacon spec/*_spec.rb
popd

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%doc %{gem_instdir}/Changelog.txt
%doc %{gem_instdir}/README.txt
%{gem_libdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.0-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5.0-2
- Rebuilt for Ruby 1.9.3.

* Sat Jan 07 2012 <stahnma@fedoraproject.org> - 0.5.0-1
- Fix bug #715948

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.4.1-2
- Fixes from Review
- Enabled %%check

* Fri Sep 03 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.4.1-1
- Initial package
