%global gem_name term-ansicolor

Summary:        Ruby library that colors strings using ANSI escape sequences
Name:           rubygem-%{gem_name}
Version:        1.3.0
Release:        6%{?dist}
Group:          Development/Languages
License:        GPLv2
URL:            http://flori.github.com/term-ansicolor
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(minitest) > 5
BuildArch:      noarch

%description
This library uses ANSI escape sequences to control the attributes of terminal
output

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c  -T
%gem_install -n %{SOURCE0}


%build


%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# removing cdiff and decolor due to file conflict with colordiff package
# mkdir -p %{buildroot}%{_bindir}
# cp -pa .%{_bindir}/* \
#         %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
rm -f %{buildroot}%{gem_instdir}/bin/cdiff

# Fix permissions.
# https://github.com/flori/term-ansicolor/pull/19
chmod a-x %{buildroot}%{gem_instdir}/{CHANGES,VERSION,Rakefile,./examples/example.rb,README.rdoc,COPYING}

# Remove empty hidden file.
rm %{buildroot}%{gem_libdir}/term/ansicolor/.keep


%check
pushd %{buildroot}%{gem_instdir}
# To run the tests using minitest 5
ruby -Ilib:tests -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end

  end

  Test = Minitest

  module Minitest::Assertions
    alias :assert_raise :assert_raises
    alias :assert_not_equal :refute_equal
  end

  Dir.glob "./tests/**/*_test.rb", &method(:require)
EOF
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%exclude %{gem_instdir}/.gitignore
%{gem_libdir}/
%{gem_instdir}/bin/
%exclude %{gem_instdir}/.travis.yml
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/VERSION
%{gem_instdir}/examples
%{gem_instdir}/tests
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/term-ansicolor.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.0-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.0-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.0-3
- Fix FTBFS in Rawhide (rhbz#1107255).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.0-1
- Update to term-ansicolor 1.3.0.

* Fri Aug 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Add rubygem-tins dependency (rhbz#972544).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.7-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.7-3
- Rebuilt for Ruby 1.9.3.
- Introduced %%check section for running tests.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.0.7-1
- updated to latest version

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.0.6-2
- removed cdiff/decolor due to conflict with colordiff package

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 1.0.6-1
- New version

* Mon Mar 07 2011 Michal Fojtik <mfojtik@redhat.com> - 1.0.5-1
- Version bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.0.3-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.0.3-2
- Fix up documentation list
- Use gem_instdir macro where appropriate
- Do not move examples around
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.0.3-1
- Package generated by gem2rpm
- Strip useless shebangs
- Move examples into documentation
- Fix up License
