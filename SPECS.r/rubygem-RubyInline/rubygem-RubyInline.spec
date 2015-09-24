# Generated from RubyInline-3.8.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name RubyInline


Summary: Write foreign code within your ruby code
Name: rubygem-%{gem_name}
Version: 3.11.3
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.zenspider.com/ZSS/Products/RubyInline/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygem(ZenTest)
Requires: gcc, ruby-devel
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(ZenTest)
BuildRequires: rubygem(minitest)
BuildRequires: ruby-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Inline allows you to write foreign code within your ruby code. It
automatically determines if the code in question has changed and
builds it only when necessary. The extensions are then automatically
loaded into the class/module that defines it.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%build
%gem_install -n %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# These are all over the map - some executable that shouldn't be, needless
# shebangs, etc. Drop all the shebangs and set a standard permission.
find %{buildroot}%{gem_instdir} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{gem_instdir} -type f | \
  xargs chmod 0644

%clean
rm -rf %{buildroot}

%check
pushd .%{gem_instdir}
ruby -Ilib -I. -e 'require "test/test_inline.rb"'
popd

%files
%defattr(-,root,root,-)
%exclude %{gem_instdir}/.gemtest
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/demo
%{gem_instdir}/example2.rb
%{gem_instdir}/example.rb
%{gem_instdir}/tutorial
%{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 3.11.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Mo Morsi <mmorsi@redhat.com> - 3.11.3-1
- new upstream version

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 3.11.0-1
- Rebuilt for Ruby 1.9.3.
- Updated to RubyInline 3.11.0.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 3.8.4-3
- replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 24 2010 Matthew Kent <mkent@magoazul.com> - 3.8.4-1
- New upstream version.

* Thu Nov 26 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-4
- Add Requires for gcc and ruby-devel, library useless without them.

* Thu Nov 26 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-3
- Drop redundant BR for gcc (#540791)
- Leave examples as upstream intended (#540791)

* Mon Nov 23 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-2
- Remove unused ruby_sitelib macro

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 3.8.3-1
- Initial package
