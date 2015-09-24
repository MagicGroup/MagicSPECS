# Generated from text-format-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name text-format

Summary: Text::Format formats fixed-width text nicely
Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 13%{?dist}
Group: Development/Languages
License: Ruby
URL: https://github.com/halostatue/text-format
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

# text-hyphen currently has an ugly license situation
# (not necessarily unacceptable for Fedora, but needs
#  looking into, remove dependency for now)
Patch0: remove-text-hyphen-dep.patch

BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Text::Format is provides the ability to nicely format fixed-width text with
knowledge of the writeable space (number of columns), margins, and indentation
settings. Text::Format can work with either TeX::Hyphen or Text::Hyphen to
hyphenate words when formatting.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_dir}
%patch0 -p0

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}

# remove installer as its not needed
pushd %{buildroot}%{gem_instdir}
rm pre-setup.rb setup.rb metaconfig

# remove dos end of line encoding
tr -d '\r' < Rakefile > Rakefile.new
mv Rakefile.new Rakefile

iconv -f iso8859-1 -t utf-8 README > README.conv && mv -f README.conv README

popd

%check
pushd %{buildroot}%{gem_instdir} 
ruby -Ilib tests/tc_*
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/Changelog
%doc %{gem_instdir}/Install
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/ToDo
%doc %{gem_instdir}/tests
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Thu Jul 31 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.0-13
- Fix FTBFS in Rawhide (rhbz#1107258).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-10
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-5
- remove extraneous file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-3
- remove 'file-not-utf8' rpmlint error

* Tue Feb 01 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-2
- Updates based on review feedback

* Tue Jan 11 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.0-1
- Initial package
