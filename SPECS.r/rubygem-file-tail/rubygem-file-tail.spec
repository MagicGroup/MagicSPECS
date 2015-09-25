# Generated from file-tail-1.0.5.gem by gem2rpm -*- rpm-spec -*-
%define gem_name file-tail

Summary: File::Tail for Ruby
Name: rubygem-%{gem_name}
Version: 1.0.12
Release: 3%{?dist}
Group: Development/Languages
License: GPLv2
URL: http://flori.github.com/file-tail
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby rubygems-devel
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
Library to tail files in Ruby


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Install rtail RubyGems stub.
sed -i '/s\.test_files/a \  s.executables = ["rtail"]' %{gem_name}.gemspec

# Relax tins dependency.
sed -i 's/%q<tins>, \["~> 0.5"\]/%q<tins>, [">= 0.5"]/' %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# rpmlint issue
find %{buildroot}%{gem_instdir}/tests -type f | \
        xargs sed -i -e '\@^#!/usr.*ruby@d'

%check
pushd .%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./tests/**/test_*.rb", &method(:require)'
popd

%files
%{_bindir}/rtail
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/file-tail.gemspec
%{gem_libdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/VERSION
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/examples
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/tests


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.12-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 23 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.12-1
- Update to file-tails 1.0.12.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Peng Wu <pwu@redhat.com> - 1.0.5-8
- Fixes build

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.5-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 21 2011  Peng Wu <pwu@redhat.com> - 1.0.5-3
- Run test suite

* Wed Apr 20 2011  Peng Wu <pwu@redhat.com> - 1.0.5-2
- Fixes the spec

* Wed Apr 20 2011 Peng Wu <pwu@redhat.com> - 1.0.5-1
- Initial package
