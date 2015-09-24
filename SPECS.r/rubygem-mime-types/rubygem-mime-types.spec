# Generated from mime-types-1.16.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mime-types


Summary: Return the MIME Content-Type for a given filename
Name: rubygem-%{gem_name}
Version: 1.25.1
Release: 3%{?dist}
Group: Development/Languages
License: GPL+ or Ruby or Artistic
URL: http://mime-types.rubyforge.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
MIME::Types for Ruby manages a MIME Content-Type database that will return the
Content-Type for a given filename.

MIME::Types was originally based on and synchronized with MIME::Types for
Perl by Mark Overmeer, copyright 2001 - 2009. As of version 1.15, the data
format for the MIME::Type list has changed and the synchronization will no
longer happen.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# These aren't executables
find %{buildroot}%{gem_instdir}/{Rakefile,test} -type f | \
  xargs -n 1 sed -i  -e '/^#! \/usr\/bin\/env .*/d'

%check
pushd .%{gem_instdir}
ruby -Ilib -rminitest/autorun -rfileutils -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Licence.rdoc
%dir %{gem_instdir}/docs
%doc %{gem_instdir}/docs/COPYING.txt
%doc %{gem_instdir}/docs/artistic.txt
%doc %{gem_instdir}/README.rdoc
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/Contributing.rdoc
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/Manifest.txt
%{gem_instdir}/test
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.25.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 1.25.1-1
- Update to mime-types 1.25.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.19-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Vít Ondruch <vondruch@redhat.com> - 1.19-1
- Update to mime-types 1.19.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.16-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 1.16-5
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 30 2009 Matthew Kent <mkent@magoazul.com> - 1.16-3
- Remove needless rcov task in Rakefile causing issue (#544964).

* Sun Dec 27 2009 Matthew Kent <mkent@magoazul.com> - 1.16-2
- Fix license (#544964).
- Add note about rcov warning in test phase (#544964).

* Sun Dec 06 2009 Matthew Kent <mkent@magoazul.com> - 1.16-1
- Initial package
