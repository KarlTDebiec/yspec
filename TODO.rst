To Do
=====

Present Tasks
-------------
- [✓] SortPlugin: Implement
- [✓] SortPlugin: Add some support for manual ordering
- [✓] PresetsPlugin: Set global preset manually
- [✓] PresetsPlugin: Reimplement support for preset inheritance and extension
- [✓] PresetsPlugin: Reimplement support for verbose preset output
- [✓] Plugin order in help text

Future Tasks
------------
- [ ] Start documentation
- [ ] Track argument access as well as origin
- [ ] YSpecConstructor: Set plugin selection and order from command line
- [ ] DefaultsPlugin: Read defaults from file
- [ ] DefaultsPlugin: Track path (for consistency)
- [ ] PresetsPlugin: Simplify to single loop?
- [ ] PresetsPlugin: Read available presets from file
- [ ] PresetsPlugin: Mutual exclusivity
- [ ] PresetsPlugin: Reimplement help table; format nested extension help
- [ ] SortPlugin: Track path (for consistency)
- [ ] WritePlugin: Implement; polish yaml_dump
- [ ] yaml_dump: Arguments to enable/disable annotation and set column number

Potenial Future Tasks
---------------------
- [ ] ArgsPlugin: Implement; accept arguments for terminal
- [ ] Store argument origin (and usage) separately from comment (but similarly)
  by subclassing classes from ruamel
- [ ] ManualPlugin: Flag to expand environment variables
- [ ] ManualPlugin: Option to keep slices in final spec

Completed Tasks
---------------

Minor Issues
------------
- Keys set to [] do not retain comment
